# Experiment 2: does an aroused fly react faster to a threat?

Blog post: link coming soon

## What this tests

Whether octopamine, the fly's arousal neurohormone, speeds up the escape circuit built in experiment 1, and if so, which real synaptic connection actually carries the effect.

## The real connections found

The connectome shows 33 real octopamine neurons (out of 126 total octopaminergic neurons in this connectome) with direct synaptic connections into three separate points along the escape pathway: onto LC4 itself, onto the upstream motion-detecting cells T4 and T2, and onto the relay cells (Tm3, T2a, T2, TmY3) between Mi1 and LC4.

## Result

Ran the same growing-threat test as experiment 1, 30 trials with the 33 octopamine neurons off, 30 with them on (15mV, same as the visual drive). With octopamine off: 37.6° ± 2.0° (matches experiment 1). With octopamine on: 31.8° ± 1.4°, firing earlier.

Isolated which of the three real connections was responsible by cutting each one individually and rerunning the full 30-trial test on each modified connectome:

| condition | mean trigger angle | std |
|---|---|---|
| octopamine on, all wires intact | 31.8° | 1.4° |
| octopamine on, LC4 connection cut | 32.5° | 1.4° |
| octopamine on, T4/T2 connection cut | 31.7° | 1.5° |
| octopamine on, relay-cell connection cut | 36.4° | 1.9° |

Cutting the relay-cell connection brings the result most of the way back to the no-octopamine baseline (37.6°). The other two cuts barely move it. The real driver is octopamine's connection into the relay cells, not LC4, which was the original assumption.

## Reproducing

```bash
# baseline (octopamine off) is experiment 1's own result, same connectome, different stimulus file

# octopamine on, intact
python ../../core/simulate.py \
  --edges ../../core/data/connectome_flight_escape.csv --neurons ../../core/data/connectome_flight_escape_neurons.csv \
  --stimulus-sequence stimuli/seq_growing_withOA.npy --stimulus-sequence-bodyids stimuli/seq_growing_withOA_bodyids.csv \
  --frame-duration 10 --duration 6000 --input-current 15 --noise-sigma 0.5 --seed 1 \
  --spike-summary-out results/intact/spike_summary_seed1.csv --spike-times-out results/intact/spike_times_seed1.csv

# repeat with --edges data/connectome_no_OA_LC4.csv, data/connectome_no_T4_T2.csv, data/connectome_no_OA_relays.csv
# for the three isolation conditions, and --seed 2 through 30 for each
```

## Contents

- `data/` — the three isolation-study connectomes, each with one of the three candidate octopamine connections removed, plus the octopamine-specific build artifacts (`oa_neuron_ids.csv`, etc.). The base connectome itself is in `core/data/`, shared with experiment 1.
- `stimuli/` — the growing-threat stimulus with the 33 octopamine neurons added to the driven set.
- `results/{intact,no_OA_LC4,no_T4_T2,no_OA_relays}/` — real per-seed spike summaries and spike times for all four conditions, N=30 each.
