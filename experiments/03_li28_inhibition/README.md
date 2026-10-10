# Experiment 3: hitting the brakes with Li28

Blog post: [Hitting the Brakes](https://pravinposts.substack.com/p/hitting-the-brakes?r=9oe50)

## What this tests

Experiments 1 and 2 only ever boosted the escape circuit (octopamine made the
sim-fly react faster). This experiment asks the opposite question: what
happens when something *inhibits* it?

The escape circuit fires once an approaching object looks big enough. But a
fly's own forward motion can make a stationary object look like it's growing
too, for the same reason an approaching one does. So the circuit needs
something to suppress it during ordinary flight, or it would trigger false
escape jumps constantly.

## The real connection found

The connectome shows over 300 real inhibitory inputs feeding into this
circuit at various stages. Out of these, we picked **Li28** — a real,
13-neuron GABAergic population wired directly onto LC4, the escape
circuit's looming detector, driven mainly by real synapses from Tm3 (its
dominant real input).

## Result

Getting Li28 to fire naturally through its own visual wiring turned out to
be a much harder, separate problem (it only gets excited very late in a
threat approach, well after the decision would already be made). So instead
we activated Li28 directly, giving it its own constant current for the
whole trial — the same approach used for the octopamine neurons in
experiment 2, and the same way real researchers use optogenetics to force a
specific neuron on regardless of what would normally trigger it.

Same method as experiments 1 and 2: 30 noise-seeded trials, same
growing-threat stimulus, same connectome.

| condition | DNp01 (decision neuron) fires at | TTMn (jump muscle neuron) fires at |
|---|---|---|
| baseline (experiment 1, no Li28) | 37.6° | ~49° |
| Li28 forced active | **90.0° ± 5.4°** | **104.1° ± 4.5°** |

With Li28 active, the sim-fly's reaction is delayed until the incoming
object covers roughly twice as much of its visual field as the unmodified
baseline — a real, falsifiable result: a living fly with Li28 activated
optogenetically should show the same delay.

## Reproducing

```bash
# 1. Pull Li28's real neurons and its real Tm3->Li28 / Li28->LC4 edges
python fetch_li28.py

# 2. Merge Li28 into the existing escape circuit (experiments 01/02's connectome)
python build_li28_connectome.py

# 3. Build the forced-activation stimulus (growing threat + Li28 given its own constant current)
python build_li28_driven_stimulus.py

# 4. Run the test (seed 1 shown; repeat --seed 2 through 30 for the full set)
python ../../core/simulate.py \
  --edges data/connectome_li28_intact.csv --neurons data/connectome_li28_intact_neurons.csv \
  --stimulus-sequence stimuli/seq_growing_plus_li28_driven.npy --stimulus-sequence-bodyids stimuli/seq_growing_plus_li28_driven_bodyids.csv \
  --frame-duration 10 --duration 6000 --input-current 15 --noise-sigma 0.5 --seed 1 \
  --spike-summary-out results/li28_forced_driven/spike_summary_seed1.csv --spike-times-out results/li28_forced_driven/spike_times_seed1.csv
```

Step 1 requires a neuprint API token (see the main repo README).

## Contents

- `fetch_li28.py`, `build_li28_connectome.py`, `build_li28_driven_stimulus.py` — the three build steps above.
- `data/` — Li28's real neurons and edges, and the merged connectome (base escape circuit + Li28).
- `stimuli/` — the forced-activation stimulus (growing threat + Li28 driven).
- `results/li28_forced_driven/` — real per-seed spike summaries and spike times, N=30.
- `images/three_panel_plate.png` — the real eye-coverage progression lined up against all three experiments' trigger-angle distributions (baseline, octopamine, Li28), `make_three_panel_plate.py` regenerates it from a saved per-seed angle summary.
