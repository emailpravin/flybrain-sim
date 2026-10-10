"""Optogenetic-style activation: give Li28 its own constant driven current
for the whole trial (same approach used for the octopamine neurons in
experiment 2), on top of the normal growing-threat stimulus driving Mi1.
Bypasses Li28's real but very-late natural recruitment through Tm3, to
test whether its real inhibitory synapse onto LC4 actually suppresses the
circuit when it is genuinely active."""
import numpy as np
import pandas as pd

growing = np.load("../01_escape_circuit/stimuli/seq_escape_test.npy")
growing_ids = pd.read_csv("../01_escape_circuit/stimuli/seq_escape_test_bodyids.csv")["bodyId"].tolist()
li28_ids = pd.read_csv("data/li28_neurons.csv")["bodyId"].tolist()

n_frames = growing.shape[0]
li28_cols = np.ones((n_frames, len(li28_ids)), dtype=np.float32)  # constant full-strength drive, every frame
combined = np.concatenate([growing, li28_cols], axis=1)
combined_ids = growing_ids + li28_ids

np.save("stimuli/seq_growing_plus_li28_driven.npy", combined)
pd.DataFrame({"bodyId": combined_ids}).to_csv("stimuli/seq_growing_plus_li28_driven_bodyids.csv", index=False)
print(f"saved {combined.shape}, {len(li28_ids)} Li28 neurons added as constantly-driven")
