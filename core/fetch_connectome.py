"""
Pull a slice of the male fruit fly CNS connectome from neuprint and save it
as a local connectivity table (CSV) for the LIF simulator to consume.

Requires a personal API token:
  1. Log into https://neuprint.janelia.org with your Google account
  2. Account menu (top right) -> copy your auth token
  3. export NEUPRINT_APPLICATION_CREDENTIALS=<paste token here>

Usage:
  # Generic slice by brain region
  python fetch_connectome.py --roi AME_R --limit 2000

  # Loom/predator-response circuit: LC4 + LC6 are the fly's visual
  # "something big is approaching" detector neurons -- closest real
  # analogue to "reacts to a spider"
  python fetch_connectome.py --types LC4,LC6 --expand-downstream --out connectome_loom.csv

  # Scaled up: follow the circuit multiple synaptic hops downstream
  # (toward descending neurons / motor output), capped so it stays tractable
  python fetch_connectome.py --types LC4,LC6 --hops 3 --max-neurons 20000 --out connectome_loom_big.csv

  python fetch_connectome.py --all            # full dataset (166k neurons, slow, needs token)
"""
import argparse
import json
import os
import sys

import pandas as pd


def primary_roi(roi_info_json):
    """Pick the ROI where a neuron has the most pre+post synapses."""
    try:
        info = json.loads(roi_info_json) if isinstance(roi_info_json, str) else roi_info_json
    except (TypeError, ValueError):
        return None
    if not info:
        return None
    best_roi, best_count = None, -1
    for roi, counts in info.items():
        total = counts.get("pre", 0) + counts.get("post", 0)
        if total > best_count:
            best_roi, best_count = roi, total
    return best_roi


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--roi", default=None, help="Restrict seed neurons to this brain region (ROI), e.g. AME_R")
    parser.add_argument("--types", default=None, help="Comma-separated cell types to use as seed/input neurons, e.g. LC4,LC6")
    parser.add_argument("--seed-file", default=None, help="CSV with a bodyId column to use as the exact seed neuron set")
    parser.add_argument("--limit", type=int, default=2000, help="Max seed neurons to pull (ignored with --all)")
    parser.add_argument("--expand-downstream", action="store_true",
                         help="Also pull neurons downstream of the seed set so activity has somewhere to propagate to (equivalent to --hops 1)")
    parser.add_argument("--hops", type=int, default=0,
                         help="Follow N synaptic hops downstream of the seed set before pulling the final adjacency (scales the network up)")
    parser.add_argument("--max-neurons", type=int, default=20000,
                         help="Safety cap on total neurons collected during hop expansion")
    parser.add_argument("--all", action="store_true", help="Pull the entire connectome (slow, large)")
    parser.add_argument("--out", default="connectome.csv", help="Output CSV path for the edge list")
    args = parser.parse_args()

    token = os.environ.get("NEUPRINT_APPLICATION_CREDENTIALS")
    if not token:
        print(
            "No NEUPRINT_APPLICATION_CREDENTIALS found.\n"
            "Get a token from https://neuprint.janelia.org (Account menu -> auth token),\n"
            "then run: export NEUPRINT_APPLICATION_CREDENTIALS=<token>\n",
            file=sys.stderr,
        )
        sys.exit(1)

    from neuprint import Client, fetch_adjacencies, fetch_neurons, NeuronCriteria as NC

    client = Client("https://neuprint.janelia.org", dataset="male-cns:v1.0", token=token)
    print(f"Connected to neuprint: {client.fetch_version()}")

    if args.all:
        criteria = NC()
    elif args.seed_file:
        seed_ids = pd.read_csv(args.seed_file)["bodyId"].tolist()
        criteria = NC(bodyId=seed_ids)
        print(f"Using {len(seed_ids)} seed neurons from {args.seed_file}")
    elif args.types:
        types = [t.strip() for t in args.types.split(",")]
        criteria = NC(type=types)
    elif args.roi:
        criteria = NC(rois=args.roi, limit=args.limit)
    else:
        criteria = NC(limit=args.limit)

    hops = max(args.hops, 1 if args.expand_downstream else 0)

    if hops > 0:
        print(f"Expanding {hops} synaptic hop(s) downstream from the seed set (cap {args.max_neurons} neurons)...")
        seed_df, _ = fetch_adjacencies(criteria, None, min_total_weight=1)
        body_ids = set(seed_df["bodyId"].tolist())
        frontier = body_ids
        for hop in range(hops):
            if len(body_ids) >= args.max_neurons:
                print(f"Hit --max-neurons cap ({args.max_neurons}) after {hop} hop(s), stopping expansion")
                break
            hop_neurons, _ = fetch_adjacencies(NC(bodyId=list(frontier)), None, min_total_weight=1)
            new_ids = set(hop_neurons["bodyId"].tolist()) - body_ids
            print(f"  hop {hop + 1}: +{len(new_ids)} new neurons (total {len(body_ids) + len(new_ids)})")
            if not new_ids:
                break
            body_ids |= new_ids
            frontier = new_ids
            if len(body_ids) > args.max_neurons:
                body_ids = set(list(body_ids)[: args.max_neurons])
                break
        print(f"Pulling final adjacency among {len(body_ids)} neurons...")
        final_criteria = NC(bodyId=list(body_ids))
        neurons_df, conn_df = fetch_adjacencies(final_criteria, final_criteria)
    else:
        print("Fetching neurons + synaptic adjacency (this can take a while)...")
        neurons_df, conn_df = fetch_adjacencies(criteria, criteria)

    print("Fetching per-ROI synapse breakdown + neurotransmitter predictions...")
    nt_props_df, roi_counts_df = fetch_neurons(NC(bodyId=neurons_df["bodyId"].tolist()))
    roi_counts_df["total"] = roi_counts_df["pre"].fillna(0) + roi_counts_df["post"].fillna(0)
    primary = (
        roi_counts_df.sort_values("total", ascending=False)
        .drop_duplicates(subset="bodyId", keep="first")[["bodyId", "roi"]]
        .rename(columns={"roi": "region"})
    )
    neurons_df = neurons_df.merge(primary, on="bodyId", how="left")
    neurons_df = neurons_df.merge(nt_props_df[["bodyId", "predictedNt"]], on="bodyId", how="left")

    INHIBITORY_NTS = {"gaba", "glutamate"}
    nt_sign = neurons_df.set_index("bodyId")["predictedNt"].str.lower().map(
        lambda nt: -1.0 if nt in INHIBITORY_NTS else 1.0
    )
    conn_df["nt_sign"] = conn_df["bodyId_pre"].map(nt_sign).fillna(1.0)
    conn_df["weight"] = conn_df["weight"] * conn_df["nt_sign"]
    conn_df = conn_df.drop(columns=["nt_sign"])
    print(f"Neurotransmitter sign breakdown among edges: "
          f"{(conn_df['weight'] > 0).sum()} excitatory, {(conn_df['weight'] < 0).sum()} inhibitory")

    conn_df = conn_df.merge(
        neurons_df[["bodyId", "type", "instance"]].rename(
            columns={"bodyId": "bodyId_pre", "type": "type_pre", "instance": "instance_pre"}
        ),
        on="bodyId_pre",
        how="left",
    ).merge(
        neurons_df[["bodyId", "type", "instance"]].rename(
            columns={"bodyId": "bodyId_post", "type": "type_post", "instance": "instance_post"}
        ),
        on="bodyId_post",
        how="left",
    )

    conn_df.to_csv(args.out, index=False)
    neurons_out = args.out.replace(".csv", "_neurons.csv")
    neurons_df.to_csv(neurons_out, index=False)
    print(f"Saved {len(neurons_df)} neurons (-> {neurons_out}) and {len(conn_df)} synaptic edges (-> {args.out})")
    if args.types:
        seed_ids = neurons_df.loc[neurons_df["type"].isin([t.strip() for t in args.types.split(",")]), "bodyId"]
        print(f"Seed/input neuron bodyIds ({args.types}): {list(seed_ids)[:20]}{'...' if len(seed_ids) > 20 else ''}")
        print("Pass these as --input-ids to simulate.py to drive exactly this circuit.")


if __name__ == "__main__":
    main()
