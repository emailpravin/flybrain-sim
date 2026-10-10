# flybrain-sim

A spiking simulation of parts of a real fruit fly's nervous system, built directly from the male-cns:v1.0 connectome (Google Research / Janelia, 2026) plus real electrical properties pulled from published electrophysiology (Shiu et al. 2024 and others). The goal: take a real wiring diagram of a real animal's brain, add real electrical properties measured in separate papers, and see whether the resulting circuit behaves like the real thing, then use it to generate real, falsifiable predictions about circuitry that hasn't been tested yet.

Three experiments so far, each written up as its own blog post.

## Experiments

### [01_escape_circuit](experiments/01_escape_circuit/) — does a connectome-based circuit actually behave like a real fly?

Builds the real visual-looming escape pathway (Mi1 → relay cells → LC4 → DNp01 → TTMn) and tests it against a simulated object approaching the fly. Confirmed the circuit fires in the real order, at roughly the real visual threshold reported in Card & Dickinson (2008), and found an emergent, unprogrammed "cliff" threshold in the process.

Blog post: [Making a simulated fly](https://pravinposts.substack.com/p/making-a-simulated-fly?r=9oe50)

### [02_octopamine_escape](experiments/02_octopamine_escape/) — does an aroused fly react faster to a threat?

Tests whether octopamine, the fly's arousal chemical, speeds up the escape circuit built in experiment 1. Finds a real effect, then isolates which of three real candidate connections actually carries it, cutting each one individually and rerunning the full test.

Blog post: link coming soon

### [03_li28_inhibition](experiments/03_li28_inhibition/) — what happens when something inhibits the escape circuit?

Experiments 1 and 2 only ever boosted the circuit. This one finds a real inhibitory wire instead: Li28, a 13-neuron GABAergic population wired directly onto the looming detector, LC4. Activates it directly (the same way the octopamine neurons were activated in experiment 2) and finds a large, real, falsifiable effect on when the sim-fly reacts.

Blog post: [Hitting the Brakes](https://pravinposts.substack.com/p/hitting-the-brakes?r=9oe50)

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Get a personal API token from [neuprint.janelia.org](https://neuprint.janelia.org) (Account menu → auth token), then:

```bash
echo "NEUPRINT_APPLICATION_CREDENTIALS=<your token>" > .env
```

Scripts in `core/` load this automatically. Never commit `.env`, it's already in `.gitignore`.

## Structure

- `core/` — the simulator (`simulate.py`, a Brian2-based leaky-integrate-and-fire network) and the scripts that fetch connectome data and build visual stimuli.
- `experiments/<name>/data/` — the real connectome edge lists used for that experiment, fetched from neuprint.
- `experiments/<name>/stimuli/` — the generated visual stimulus sequences.
- `experiments/<name>/results/` — real simulation output (per-seed spike summaries and spike times) for the numbers reported in that experiment's blog post.
- `research_log.md` — the full, chronological lab notebook behind both experiments, every finding, correction, and dead end along the way.
