# Experiment 1: the escape circuit

Blog post: [Making a simulated fly](https://pravinposts.substack.com/p/making-a-simulated-fly?r=9oe50)

## What this tests

Whether a real connectome, combined with real electrical properties from separate published papers, produces a circuit that behaves like a real fly when shown a simulated approaching threat.

## The circuit

Mi1 (317 driven visual input neurons) → Tm3, T2a, T2, TmY3 (real motion relays) → LC4 (looming detector) → DNp01 (escape command cell) → TTMn (jump muscle), all real connections from male-cns:v1.0.

## Result

Ran 30 noise-seeded trials of a simulated object approaching the fly (real time-to-collision physics, tau=159.5ms, start=3°, end=120°). The escape circuit fired in the correct real order in every trial, and triggered at a mean of 37.6° ± 2.0° of eye coverage (range 33.5°–42.1°), matching the real 30–40° threshold reported in Card & Dickinson (2008), *Journal of Experimental Biology* 211:341-353.

Separately found a sharp, unprogrammed "cliff": a non-moving control object never triggers the circuit below 16mV of input current, then triggers it constantly at 17mV, an emergent threshold effect, not something explicitly coded.

## Reproducing

```bash
python ../../core/simulate.py \
  --edges ../../core/data/connectome_flight_escape.csv --neurons ../../core/data/connectome_flight_escape_neurons.csv \
  --stimulus-sequence stimuli/seq_escape_test.npy --stimulus-sequence-bodyids stimuli/seq_escape_test_bodyids.csv \
  --frame-duration 10 --duration 6000 --input-current 15 --noise-sigma 0.5 --seed 1 \
  --spike-summary-out results/spike_summary_seed1.csv --spike-times-out results/spike_times_seed1.csv
```

Repeat with `--seed 2` through `--seed 30` to regenerate the full set in `results/`.

Note: this experiment uses the same combined connectome (`core/data/connectome_flight_escape.csv`, 3,169 neurons, 76,257 edges) as experiment 2, shared because the real escape-circuit numbers reported in both blog posts were generated on this one connectome, not the smaller, earlier `connectome_escape.csv` build from before the flight-state circuitry was merged in.

## Contents

- `stimuli/` — the growing-threat stimulus (`seq_escape_test.npy`) and the stationary-object control (`seq_stationary_blob.npy`), both built from real time-to-collision physics.
- `results/` — real per-seed spike summaries and spike times from the N=30 run reported above.
- `images/` — the eye-view visualizations and figures used in the blog post.
- The connectome itself lives in `core/data/`, shared with experiment 2.
