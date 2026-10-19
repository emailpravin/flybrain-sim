"""Build the N=30 per-trial spike-count JSON for the cardinal plate,
from the real final-N30 run (run_t4_final_n30.sh output), counting each
subtype's own real spikes only -- same convention as the original N=10
t4_cardinal_per_trial_FINAL.json."""
import json
import numpy as np
import pandas as pd
from scipy import stats

SUBS = ["T4a", "T4b", "T4c", "T4d"]
out = {}
for sub in SUBS:
    out[sub] = {}
    for cond in ["pref", "anti"]:
        counts = []
        for seed in range(1, 31):
            df = pd.read_csv(f"/tmp/t4_final_n30/{sub}_{cond}_seed{seed}.csv")
            counts.append(int((df.type == sub).sum()))
        out[sub][cond] = counts

json.dump(out, open("data_full/t4_cardinal_per_trial_N30.json", "w"), indent=1)
print("saved data_full/t4_cardinal_per_trial_N30.json")

for sub in SUBS:
    pref = np.array(out[sub]["pref"], dtype=float)
    anti = np.array(out[sub]["anti"], dtype=float)
    diff_pct = (pref.mean() - anti.mean()) / anti.mean() * 100
    t, p = stats.ttest_ind(pref, anti)
    print(f"{sub}: pref={pref.mean():.1f} anti={anti.mean():.1f} diff={diff_pct:.1f}% p={p:.2e}")
