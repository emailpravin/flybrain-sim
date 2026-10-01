"""
Leaky integrate-and-fire (LIF) simulation running on a connectome edge list.

Reads a CSV with columns: bodyId_pre, bodyId_post, weight (signed: positive =
excitatory, negative = inhibitory synapse), stimulates a set of "input"
neurons with a driving current, lets activity propagate through the wired-up
network, and plots:
  1. a raster of spikes
  2. a population firing-rate trace
  3. (if a neurons CSV with a "region" column is given) a bar chart of which
     brain region fired the most -- i.e. "what part of the brain reacted"

Usage:
  # generic / synthetic data, random input neurons
  python simulate.py --edges connectome_synthetic.csv --duration 200 --n-inputs 10

  # real connectome, explicit "threat detector" cell types as input,
  # regions broken out by brain area
  python simulate.py --edges connectome_loom.csv --neurons connectome_loom_neurons.csv \\
      --input-types LC4,LC6 --duration 300
"""
import argparse

import numpy as np
import pandas as pd
from brian2 import (
    NeuronGroup, Synapses, SpikeMonitor, PopulationRateMonitor,
    TimedArray, run, ms, mV, defaultclock, Hz, seed as brian_seed,
)


def build_network_dynamic(edges_df, stim_array, stim_bodyids, frame_duration_ms, input_current_mV,
                           synapse_mV=0.275, synapse_clip=100000, v_thresh_mV=-45, v_rest_mV=-52,
                           tau_adapt_ms=0, adapt_strength_mV=0, refractory_ms=2.2,
                           tau_mbr_ms=20, tau_syn_ms=5, syn_delay_ms=1.8, type_boost=None,
                           noise_sigma_mV=0.0, weight_exponent=1.0, weight_exponent_ref=20.0,
                           per_id_current_scale=None):
    """Neuron/synapse equations matching Shiu et al. 2024 (Nature) -- the
    published whole-brain Drosophila LIF model -- rather than our earlier,
    simplified instantaneous-jump synapse:

        dv/dt = (v_rest - v + g + stim) / tau_mbr
        dg/dt = -g / tau_syn                        (real synapses decay, not instant)

    with a real synaptic transmission delay (syn_delay_ms) on every
    connection. Defaults are Shiu et al.'s actual published values (v_thresh
    -45mV, v_rest -52mV, refractory 2.2ms, tau_syn 5ms, tau_mbr 20ms,
    synapse_mV 0.275mV, delay 1.8ms) -- not our own guesses.

    tau_adapt_ms/adapt_strength_mV optionally add spike-frequency adaptation
    on top (0 = disabled, matching Shiu et al., who did not use it).

    noise_sigma_mV: standard Brian2 Euler-Maruyama membrane noise term
    (sigma*xi*tau_mbr**-0.5), representing real trial-to-trial channel/
    synaptic noise that Shiu et al.'s deterministic model does not include.
    0 (default) reproduces the old fully-deterministic behavior exactly --
    every finding in this project before this parameter existed used 0."""
    body_ids = pd.unique(pd.concat([edges_df["bodyId_pre"], edges_df["bodyId_post"]]))
    body_ids.sort()
    idx = {b: i for i, b in enumerate(body_ids)}
    n = len(body_ids)
    n_frames = stim_array.shape[0]

    full_stim = np.zeros((n_frames, n), dtype=np.float32)
    input_ids = []
    for col, b in enumerate(stim_bodyids):
        if b in idx:
            scale = per_id_current_scale.get(b, 1.0) if per_id_current_scale else 1.0
            full_stim[:, idx[b]] = stim_array[:, col] * input_current_mV * scale
            input_ids.append(idx[b])
    if not input_ids:
        raise ValueError("None of the stimulus sequence bodyIds were found in this edge list")

    stim_ta = TimedArray(full_stim * mV, dt=frame_duration_ms * ms)

    adapt_term = " - adapt" if tau_adapt_ms > 0 else ""
    noise_term = " + sigma_noise*xi*tau_mbr**-0.5" if noise_sigma_mV > 0 else ""
    eqs = f"""
    dv/dt = (v_rest - v + g + stim_ta(t, i){adapt_term}) / tau_mbr{noise_term} : volt (unless refractory)
    dg/dt = -g / tau_syn : volt (unless refractory)
    v_rest : volt
    """
    reset = "v = v_reset"
    namespace = {
        "v_thresh": v_thresh_mV * mV, "v_reset": v_rest_mV * mV,
        "tau_mbr": tau_mbr_ms * ms, "tau_syn": tau_syn_ms * ms, "stim_ta": stim_ta,
    }
    if noise_sigma_mV > 0:
        namespace["sigma_noise"] = noise_sigma_mV * mV
    if tau_adapt_ms > 0:
        eqs += "dadapt/dt = -adapt / tau_adapt : volt (unless refractory)\n"
        reset += "; adapt += adapt_strength"
        namespace["tau_adapt"] = tau_adapt_ms * ms
        namespace["adapt_strength"] = adapt_strength_mV * mV

    G = NeuronGroup(
        n, eqs, threshold="v > v_thresh", reset=reset,
        method="euler", refractory=refractory_ms * ms,
        namespace=namespace,
    )
    G.v = v_rest_mV * mV
    G.v_rest = v_rest_mV * mV
    if tau_adapt_ms > 0:
        G.adapt = 0 * mV

    # A real connection between two neurons is often split across multiple
    # ROI rows in the source data (per-brain-region synapse counts). Clipping
    # each ROI row separately lets the TRUE total synapse count for a single
    # real connection blow past synapse_clip -- confirmed: 328/1092 direct
    # inputs to the two Giant Fiber neurons exceeded the intended cap of 20
    # once properly summed, one by 37x (739 real synapses). Aggregate to one
    # row per real (pre, post) connection BEFORE clipping, not after.
    agg = edges_df.groupby(["bodyId_pre", "bodyId_post"], as_index=False).agg(
        weight=("weight", "sum"), type_pre=("type_pre", "first"), type_post=("type_post", "first")
    )

    pre_idx = agg["bodyId_pre"].map(idx).to_numpy()
    post_idx = agg["bodyId_post"].map(idx).to_numpy()
    raw_weights = agg["weight"].to_numpy().astype(float)
    clipped = np.clip(np.abs(raw_weights), 0, synapse_clip) * np.sign(raw_weights)
    # weight_exponent=1.0 (default) is the original linear synapse-count-to-mV
    # mapping used throughout this project. <1.0 (e.g. 0.5 = sqrt) tests
    # sub-linear/saturating synaptic strength -- a real, documented property
    # of real synapses that this project's default linear mapping doesn't
    # capture, and for which no per-transmitter-type literature magnitude
    # exists to calibrate directly. weight_exponent_ref anchors the two
    # mappings to agree at a chosen reference synapse count (default 20,
    # this project's old default clip value) so a sweep changes ONLY the
    # curve's shape, not its overall scale at that reference point.
    if weight_exponent != 1.0:
        effective_synapse_mV = synapse_mV * (weight_exponent_ref ** (1.0 - weight_exponent))
        magnitude = np.abs(clipped) ** weight_exponent
        weights = np.sign(clipped) * magnitude * effective_synapse_mV
    else:
        weights = clipped * synapse_mV

    if type_boost:
        # Surgical, per-connection-type strength override -- e.g. boosting
        # only LC9->LC9 recurrent synapses, instead of raising synapse_mV
        # globally (which strengthens every connection including unrelated
        # circuits like the escape pathway, destroying selectivity).
        boost_mult = np.ones(len(agg), dtype=float)
        for (t_pre, t_post), mult in type_boost.items():
            mask = (agg["type_pre"] == t_pre) & (agg["type_post"] == t_post)
            boost_mult[mask.to_numpy()] = mult
        weights = weights * boost_mult

    S = Synapses(G, G, model="w : volt", on_pre="g_post += w", delay=syn_delay_ms * ms)
    S.connect(i=pre_idx, j=post_idx)
    S.w = weights * mV

    return G, S, body_ids, np.array(input_ids), n_frames * frame_duration_ms


def build_network(edges_df, input_ids_bodyids, input_current_mV, n_inputs_random, seed,
                   per_id_scale=None, synapse_mV=0.3, synapse_clip=100000):
    rng = np.random.default_rng(seed)

    body_ids = pd.unique(pd.concat([edges_df["bodyId_pre"], edges_df["bodyId_post"]]))
    body_ids.sort()
    idx = {b: i for i, b in enumerate(body_ids)}
    n = len(body_ids)

    eqs = """
    dv/dt = (v_rest - v + I) / tau : volt
    I : volt
    v_rest : volt
    """
    G = NeuronGroup(
        n, eqs, threshold="v > v_thresh", reset="v = v_reset",
        method="euler", refractory=3 * ms,
        namespace={"v_thresh": -50 * mV, "v_reset": -65 * mV, "tau": 10 * ms},
    )
    G.v = -65 * mV
    G.v_rest = -65 * mV
    G.I = 0 * mV

    if input_ids_bodyids:
        input_ids = np.array([idx[b] for b in input_ids_bodyids if b in idx])
        if len(input_ids) == 0:
            raise ValueError("None of --input-ids/--input-types bodyIds were found in the edge list")
    else:
        input_ids = rng.choice(n, size=min(n_inputs_random, n), replace=False)

    if per_id_scale:
        for b, scale in per_id_scale.items():
            if b in idx:
                G.I[idx[b]] = input_current_mV * scale * mV
        for i in input_ids:
            if body_ids[i] not in per_id_scale:
                G.I[i] = input_current_mV * mV
    else:
        G.I[input_ids] = input_current_mV * mV

    # Aggregate multi-ROI rows to one real (pre, post) connection before
    # clipping -- see build_network_dynamic for why.
    agg = edges_df.groupby(["bodyId_pre", "bodyId_post"], as_index=False)["weight"].sum()
    pre_idx = agg["bodyId_pre"].map(idx).to_numpy()
    post_idx = agg["bodyId_post"].map(idx).to_numpy()
    raw_weights = agg["weight"].to_numpy().astype(float)
    # Fixed per-synapse conductance (not normalized by the dataset's global max,
    # which is a huge outlier edge and crushes typical 1-5-synapse connections
    # to near-zero). Clip per-edge synapse count so a few outlier hub
    # connections don't single-handedly dominate.
    clipped = np.clip(np.abs(raw_weights), 0, synapse_clip) * np.sign(raw_weights)
    weights = clipped * synapse_mV

    S = Synapses(G, G, model="w : volt", on_pre="v_post += w")
    S.connect(i=pre_idx, j=post_idx)
    S.w = weights * mV

    return G, S, body_ids, input_ids


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--edges", default="connectome_synthetic.csv")
    parser.add_argument("--neurons", default=None, help="Neurons CSV (needs a 'region' column for the region bar chart)")
    parser.add_argument("--duration", type=float, default=200.0, help="Simulation duration in ms")
    parser.add_argument("--n-inputs", type=int, default=10, help="Number of RANDOM neurons to drive if no --input-ids/--input-types given")
    parser.add_argument("--input-ids", default=None, help="Comma-separated bodyIds to drive as input")
    parser.add_argument("--stimulus-csv", default=None,
                         help="CSV with columns bodyId,scale -- per-neuron stimulus (e.g. from image_to_retina.py). "
                              "Overrides --input-ids/--input-types/--type-weights.")
    parser.add_argument("--stimulus-sequence", default=None,
                         help="NPY file (n_frames x n_columns) from image_to_retina_sequence.py -- genuine "
                              "time-varying stimulus. Requires --stimulus-sequence-bodyids. Overrides everything else.")
    parser.add_argument("--stimulus-sequence-bodyids", default=None,
                         help="CSV with a bodyId column giving the column order for --stimulus-sequence")
    parser.add_argument("--frame-duration", type=float, default=50.0,
                         help="ms per frame in --stimulus-sequence (total duration = n_frames * this)")
    parser.add_argument("--input-types", default=None, help="Comma-separated cell types (requires --neurons) to drive as input")
    parser.add_argument("--type-weights", default=None,
                         help="Per-type relative stimulus scale, e.g. 'LC4:1.0,LC6:1.0,LC11:0.6' "
                              "(types not listed default to 1.0). Multiplies --input-current.")
    parser.add_argument("--input-current", type=float, default=25.0, help="Driving current in mV/tau units")
    parser.add_argument("--synapse-mv", type=float, default=0.275, help="mV of postsynaptic potential per synapse in an edge's weight (Shiu et al. 2024: 0.275mV)")
    parser.add_argument("--type-boost", default=None,
                         help="Surgical per-connection-type synapse strength multiplier, comma-separated "
                              "TypePre:TypePost:multiplier triples, e.g. 'LC9:LC9:4.0'. Unlike --synapse-mv "
                              "(which scales every synapse in the network), this only multiplies edges whose "
                              "real pre/post type match -- for testing whether a specific circuit's own "
                              "recurrent/internal connections are the bottleneck, without also strengthening "
                              "unrelated pathways.")
    parser.add_argument("--synapse-clip", type=float, default=100000,
                         help="Cap per-edge (real, ROI-aggregated) synapse count before scaling. "
                              "Default is effectively uncapped: swept 20-5000 with no instability found "
                              "(the true max single connection in every network built so far is 2591), "
                              "and swept synapse-mv 0.275-20 with the cap off with no runaway either -- "
                              "the network saturates smoothly against the refractory period instead. "
                              "The old default of 20 was never literature-grounded and was found to "
                              "silently truncate real strong connections (e.g. a real 615-synapse "
                              "courtship pathway edge) to the same size as much weaker ones. Set lower "
                              "only if you have a specific reason to reintroduce a cap.")
    parser.add_argument("--v-thresh", type=float, default=-45, help="Spike threshold in mV (Shiu et al. 2024 / real Drosophila central neurons: -45mV)")
    parser.add_argument("--v-rest", type=float, default=-52, help="Resting potential in mV (Shiu et al. 2024 / real Drosophila central neurons: -52mV)")
    parser.add_argument("--tau-adapt", type=float, default=0, help="Spike-frequency adaptation time constant in ms (0 = disabled, matches Shiu et al., who did not use adaptation)")
    parser.add_argument("--adapt-strength", type=float, default=0, help="mV added to the adaptation variable per spike (untuned -- no direct measurement found; tune to prevent runaway)")
    parser.add_argument("--refractory", type=float, default=2.2, help="Refractory period in ms (Shiu et al. 2024: 2.2ms)")
    parser.add_argument("--tau-mbr", type=float, default=20, help="Membrane time constant in ms (Shiu et al. 2024: 20ms)")
    parser.add_argument("--tau-syn", type=float, default=5, help="Synaptic decay time constant in ms (Shiu et al. 2024: 5ms)")
    parser.add_argument("--syn-delay", type=float, default=1.8, help="Synaptic transmission delay in ms (Shiu et al. 2024: 1.8ms)")
    parser.add_argument("--weight-exponent", type=float, default=1.0,
                         help="Exponent applied to real synapse count before scaling to mV. "
                              "1.0 (default) = linear, this project's original assumption. "
                              "0.5 = square-root (sub-linear/saturating), testing robustness to a "
                              "real but unquantified property of real synapses (no per-transmitter "
                              "literature magnitude exists to calibrate this directly, so this is a "
                              "sensitivity test, not a claimed-correct value).")
    parser.add_argument("--weight-exponent-ref", type=float, default=20.0,
                         help="Synapse count at which --weight-exponent's curve is anchored to match "
                              "the linear mapping exactly, so a sweep changes only the curve's shape.")
    parser.add_argument("--noise-sigma", type=float, default=0.0,
                         help="Standard deviation (mV) of real trial-to-trial membrane noise (Brian2 xi term). "
                              "0 (default) is fully deterministic, matching every finding in this project before "
                              "this flag existed. Nonzero requires --seed to vary across repeated runs to see "
                              "trial-to-trial variability -- Shiu et al.'s own model is deterministic (no noise "
                              "term), so this is an explicit addition, not a literature-matched default.")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--scale-types", default=None,
                         help="Comma-separated cell types (requires --neurons) whose driven current gets "
                              "multiplied by --scale-mult instead of the plain --input-current. Lets you "
                              "sweep one input pathway (e.g. Mi1/vision) independently of another (e.g. "
                              "ORN_VA6/smell) within the same --stimulus-sequence, since both share one "
                              "input-current value otherwise.")
    parser.add_argument("--scale-mult", type=float, default=1.0,
                         help="Multiplier applied to --input-current for neurons of --scale-types only.")
    parser.add_argument("--out", default="raster.png")
    parser.add_argument("--region-out", default="region_activation.png")
    parser.add_argument("--spike-summary-out", default=None,
                         help="Dump full per-neuron spike summary (bodyId, type, region, n_spikes, is_driven_input) to this CSV")
    parser.add_argument("--spike-times-out", default=None,
                         help="Dump every individual spike (bodyId, type, t_ms) to this CSV -- needed for spike-timing analyses (e.g. first-spike latency), unlike --spike-summary-out which only has counts")
    args = parser.parse_args()

    print(f"Loading edges from {args.edges} ...")
    edges_df = pd.read_csv(args.edges)
    n_endpoints = pd.unique(pd.concat([edges_df["bodyId_pre"], edges_df["bodyId_post"]])).shape[0]
    print(f"{n_endpoints} distinct neurons, {len(edges_df)} edges")

    neurons_df = pd.read_csv(args.neurons) if args.neurons else None

    input_ids_bodyids = []
    per_id_scale = None
    if args.stimulus_csv:
        stim_df = pd.read_csv(args.stimulus_csv)
        stim_df = stim_df[stim_df["bodyId"].isin(edges_df["bodyId_pre"]) | stim_df["bodyId"].isin(edges_df["bodyId_post"])]
        input_ids_bodyids = stim_df["bodyId"].tolist()
        per_id_scale = dict(zip(stim_df["bodyId"], stim_df["scale"]))
        print(f"Driving {len(input_ids_bodyids)} retina columns from {args.stimulus_csv} "
              f"(matched against this connectome's {n_endpoints} neurons)")
    elif args.input_ids:
        input_ids_bodyids = [int(x) for x in args.input_ids.split(",")]
    elif args.input_types:
        if neurons_df is None:
            raise ValueError("--input-types requires --neurons")
        types = [t.strip() for t in args.input_types.split(",")]
        input_ids_bodyids = neurons_df.loc[neurons_df["type"].isin(types), "bodyId"].tolist()
        print(f"Driving {len(input_ids_bodyids)} neurons of type(s) {types} as input")

    if args.type_weights and neurons_df is not None and per_id_scale is None:
        type_scale = {}
        for pair in args.type_weights.split(","):
            t, w = pair.split(":")
            type_scale[t.strip()] = float(w)
        type_of_body = dict(zip(neurons_df["bodyId"], neurons_df["type"]))
        per_id_scale = {b: type_scale.get(type_of_body.get(b), 1.0) for b in input_ids_bodyids}
        print(f"Per-type stimulus weights: {type_scale}")

    defaultclock.dt = 0.1 * ms
    brian_seed(args.seed)  # seeds Brian2's own RNG (incl. the xi noise term) -- previously unseeded

    type_boost = None
    if args.type_boost:
        type_boost = {}
        for triple in args.type_boost.split(","):
            t_pre, t_post, mult = triple.split(":")
            type_boost[(t_pre.strip(), t_post.strip())] = float(mult)
        print(f"Type-specific synapse boost: {type_boost}")

    if args.stimulus_sequence:
        stim_array = np.load(args.stimulus_sequence)
        stim_bodyids = pd.read_csv(args.stimulus_sequence_bodyids)["bodyId"].tolist()
        per_id_current_scale = None
        if args.scale_types:
            if neurons_df is None:
                raise ValueError("--scale-types requires --neurons")
            scale_type_set = {t.strip() for t in args.scale_types.split(",")}
            type_of_body = dict(zip(neurons_df["bodyId"], neurons_df["type"]))
            per_id_current_scale = {
                b: (args.scale_mult if type_of_body.get(b) in scale_type_set else 1.0)
                for b in stim_bodyids
            }
            print(f"Scaling input-current by {args.scale_mult}x for types {scale_type_set}")
        G, S, body_ids, input_idx, duration_ms = build_network_dynamic(
            edges_df, stim_array, stim_bodyids, args.frame_duration, args.input_current,
            synapse_mV=args.synapse_mv, synapse_clip=args.synapse_clip,
            v_thresh_mV=args.v_thresh, v_rest_mV=args.v_rest,
            tau_adapt_ms=args.tau_adapt, adapt_strength_mV=args.adapt_strength,
            refractory_ms=args.refractory,
            tau_mbr_ms=args.tau_mbr, tau_syn_ms=args.tau_syn, syn_delay_ms=args.syn_delay,
            type_boost=type_boost, noise_sigma_mV=args.noise_sigma,
            weight_exponent=args.weight_exponent, weight_exponent_ref=args.weight_exponent_ref,
            per_id_current_scale=per_id_current_scale,
        )
        input_ids_bodyids = list(body_ids[input_idx])
        print(f"Using time-varying stimulus: {stim_array.shape[0]} frames x {args.frame_duration}ms = {duration_ms}ms")
    else:
        G, S, body_ids, input_idx = build_network(
            edges_df, input_ids_bodyids, args.input_current, args.n_inputs, args.seed, per_id_scale,
            synapse_mV=args.synapse_mv, synapse_clip=args.synapse_clip,
        )
        duration_ms = args.duration

    spikes = SpikeMonitor(G)
    rate = PopulationRateMonitor(G)

    print(f"Running {duration_ms} ms of simulated activity on {len(body_ids)} neurons, "
          f"{len(S)} synapses, {len(input_idx)} driven input neurons...")
    run(duration_ms * ms)

    print(f"Total spikes: {spikes.num_spikes}")
    print(f"Peak population rate: {rate.smooth_rate(window='flat', width=2*ms).max():.1f}")

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 6), sharex=True)
    ax1.plot(spikes.t / ms, spikes.i, ".", markersize=2, color="black")
    ax1.scatter(
        np.zeros(len(input_idx)), input_idx, marker=">", color="red", s=30,
        label="driven input neurons", zorder=3,
    )
    ax1.set_ylabel("neuron index")
    ax1.set_title(f"Spike raster ({len(body_ids)} neurons, {len(S)} synapses)")
    ax1.legend(loc="upper right", fontsize=8)

    ax2.plot(rate.t / ms, rate.smooth_rate(window="flat", width=2 * ms) / Hz)
    ax2.set_xlabel("time (ms)")
    ax2.set_ylabel("population rate (Hz)")

    plt.tight_layout()
    plt.savefig(args.out, dpi=150)
    print(f"Saved raster plot to {args.out}")

    if neurons_df is not None and "region" in neurons_df.columns:
        input_body_id_set = set(input_ids_bodyids) if input_ids_bodyids else set(body_ids[input_idx])
        spike_body_ids = body_ids[spikes.i]
        spike_counts = pd.Series(spike_body_ids, name="bodyId").value_counts().rename_axis("bodyId").reset_index(name="n_spikes")
        merged = spike_counts.merge(neurons_df[["bodyId", "region", "type"]], on="bodyId", how="left")
        merged["is_driven_input"] = merged["bodyId"].isin(input_body_id_set)

        if args.spike_summary_out:
            merged.sort_values("n_spikes", ascending=False).to_csv(args.spike_summary_out, index=False)
            print(f"Saved full per-neuron spike summary to {args.spike_summary_out}")

        if args.spike_times_out:
            spike_types = neurons_df.set_index("bodyId")["type"].reindex(spike_body_ids).values
            times_df = pd.DataFrame({"bodyId": spike_body_ids, "type": spike_types, "t_ms": spikes.t / ms})
            times_df.sort_values("t_ms").to_csv(args.spike_times_out, index=False)
            print(f"Saved {len(times_df)} individual spike times to {args.spike_times_out}")

        n_driven_spikes = merged.loc[merged["is_driven_input"], "n_spikes"].sum()
        n_downstream_spikes = merged.loc[~merged["is_driven_input"], "n_spikes"].sum()
        n_downstream_neurons = (~merged["is_driven_input"]).sum()
        print(f"\nSpikes from the {len(input_body_id_set)} directly-driven input neurons: {n_driven_spikes}")
        print(f"Spikes from {n_downstream_neurons} OTHER (downstream, not directly driven) neurons: {n_downstream_spikes}")

        print("\nTop spiking cell TYPES among directly-driven input neurons:")
        print(merged.loc[merged["is_driven_input"]].groupby("type")["n_spikes"].sum()
              .sort_values(ascending=False).head(10).to_string())

        print("\nTop spiking cell TYPES among downstream (non-input) neurons -- this is what actually propagated:")
        downstream_by_type = merged.loc[~merged["is_driven_input"]].groupby("type")["n_spikes"].sum().sort_values(ascending=False)
        print(downstream_by_type.head(15).to_string() if len(downstream_by_type) else "  (none -- activity did not propagate beyond the driven input neurons)")

        print("\nDownstream-only spikes by region (excludes directly-driven input neurons):")
        downstream_by_region = merged.loc[~merged["is_driven_input"]].groupby("region")["n_spikes"].sum().sort_values(ascending=False)
        print(downstream_by_region.head(15).to_string() if len(downstream_by_region) else "  (none)")

        by_region = merged.groupby("region")["n_spikes"].sum().sort_values(ascending=False)

        if len(by_region):
            fig2, ax = plt.subplots(figsize=(9, max(3, 0.3 * len(by_region))))
            by_region.head(25).plot.barh(ax=ax, color="darkorange")
            ax.invert_yaxis()
            ax.set_xlabel("total spikes")
            ax.set_title("Which brain region reacted most")
            plt.tight_layout()
            plt.savefig(args.region_out, dpi=150)
            print(f"Saved region activation chart to {args.region_out}")
            print("\nTop responding regions:")
            print(by_region.head(10).to_string())
        else:
            print("\nNo spiking neurons had a tagged region -- skipping region chart.")
    elif args.neurons:
        print("Note: --neurons file has no 'region' column, skipping region chart "
              "(re-run fetch_connectome.py to regenerate it with region tagging)")


if __name__ == "__main__":
    main()
