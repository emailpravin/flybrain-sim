"""Plate: one row per T4 subtype -- an eye-view panel showing a dot
swept along that subtype's own real measured preferred angle, plus a
strip plot of the real per-trial spike counts (preferred vs. anti,
full clean N=30 per condition, run under the calibration-corrected
real spatial delay -- spatial_delays_x6.csv, confirmed via the real
grating/temporal-frequency test to land T4's speed tuning in Creamer
et al. 2018's real measured range) -- same jittered-dot / mean+/-std
diamond convention as make_steering_plate.py."""
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrow

mi1 = pd.read_csv("data_full/mi1_columns_R.csv")
trials = json.load(open("data_full/t4_cardinal_per_trial_N30.json"))
CENTER = (18.0, 20.0)
RADIUS = 20.0

subtypes = [
    {"name": "T4a", "angle": -74.1, "diff": 117.9, "p": "9.7e-65", "color": "#0050d0"},
    {"name": "T4b", "angle": 110.6, "diff": 87.6, "p": "5.2e-63", "color": "#0F6E56"},
    {"name": "T4c", "angle": -150.0, "diff": 281.1, "p": "4.6e-72", "color": "#993C1D"},
    {"name": "T4d", "angle": 31.7, "diff": 56.6, "p": "5.4e-58", "color": "#993556"},
]

fig = plt.figure(figsize=(13, 15.6))
fig.text(0.5, 0.985, "Results: Multiplicative Disinhibition Works",
          ha="center", va="top", fontsize=17, fontweight="bold")
fig.text(0.5, 0.955,
          "Just as it does in the real fly, each subtype swept along its own real measured preferred angle, N=30 trials.\n"
          "The simple additive model, tested the same way, was flat.",
          ha="center", va="top", fontsize=10.5, color="#666666", style="italic")

EYE_X, EYE_W = 0.04, 0.30
STRIP_X, STRIP_W = 0.42, 0.40
BAR_X, BAR_W = 0.85, 0.12
row_h = 0.205
row_gap = 0.015
top_y = 0.89

rng = np.random.default_rng(0)

all_trial_vals = np.concatenate([
    np.array(trials[s["name"]]["pref"] + trials[s["name"]]["anti"], dtype=float) for s in subtypes
])
GLOBAL_PAD = (all_trial_vals.max() - all_trial_vals.min()) * 0.08
GLOBAL_XLIM = (all_trial_vals.min() - GLOBAL_PAD, all_trial_vals.max() + GLOBAL_PAD)
GLOBAL_BAR_MAX = max(
    np.array(trials[s["name"]]["pref"], dtype=float).mean() for s in subtypes
) * 1.15

for i, sub in enumerate(subtypes):
    y0 = top_y - (i + 1) * row_h - i * row_gap

    # --- eye-view panel ---
    ax = fig.add_axes([EYE_X, y0, EYE_W, row_h])
    ax.scatter(mi1.hex1, mi1.hex2, s=5, c="lightgray", edgecolors="none")
    cx, cy = CENTER
    band = mi1[(mi1.hex1 - cx) ** 2 + (mi1.hex2 - cy) ** 2 <= 9 ** 2]
    ax.scatter(band.hex1, band.hex2, s=5, c="#555555", edgecolors="none")

    for ref_deg in (0, 90, 180, 270):
        rtheta = np.radians(ref_deg)
        rdx, rdy = (RADIUS + 1) * np.cos(rtheta), (RADIUS + 1) * np.sin(rtheta) * (2 / np.sqrt(3))
        ax.plot([cx, cx + rdx], [cy, cy + rdy], color="#cccccc", linewidth=0.7, linestyle=(0, (4, 3)), zorder=1)

    theta = np.radians(sub["angle"])
    dx, dy = 7 * np.cos(theta), 7 * np.sin(theta) * (2 / np.sqrt(3))
    ax.add_patch(FancyArrow(cx - dx / 2, cy - dy / 2, dx, dy, width=0.55, head_width=2.0,
                             head_length=2.2, length_includes_head=True, color=sub["color"], zorder=5))
    ax.add_patch(Circle(CENTER, RADIUS, fill=False, edgecolor="gray", linewidth=0.8))
    ax.set_xlim(cx - RADIUS - 1, cx + RADIUS + 1)
    ax.set_ylim(cy - RADIUS - 1, cy + RADIUS + 1)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.text(0.5, 1.05, f"{sub['name']}  ({sub['angle']:.0f}°)", transform=ax.transAxes, ha="center", va="bottom",
            fontsize=15, fontweight="bold", color=sub["color"])

    # --- strip plot of real per-trial spike counts ---
    axs = fig.add_axes([STRIP_X, y0 + 0.02, STRIP_W, row_h - 0.04])
    pref = np.array(trials[sub["name"]]["pref"], dtype=float)
    anti = np.array(trials[sub["name"]]["anti"], dtype=float)

    for yc, vals, label in [(0.72, pref, "preferred"), (0.22, anti, "opposite")]:
        jitter = rng.uniform(-0.09, 0.09, size=len(vals))
        axs.scatter(vals, yc + jitter, s=26, c=sub["color"], alpha=0.65 if label == "opposite" else 0.9,
                    edgecolors="none", zorder=3)
        m, s = vals.mean(), vals.std()
        axs.errorbar([m], [yc], xerr=[s], fmt="D", color="black", markersize=6, capsize=4,
                     linewidth=1.4, markeredgewidth=0, zorder=4)
        axs.text(-0.01, yc, f"{label}\n(N={len(vals)})", transform=axs.get_yaxis_transform(),
                  ha="right", va="center", fontsize=9.5)

    axs.set_xlim(*GLOBAL_XLIM)
    axs.set_ylim(0, 1)
    axs.set_yticks([])
    axs.spines[["top", "right", "left"]].set_visible(False)
    axs.tick_params(axis="x", labelsize=9)
    if i == len(subtypes) - 1:
        axs.set_xlabel("real T4 spike count per trial", fontsize=11)
    spike_diff = pref.mean() - anti.mean()
    axs.text(1.0, 1.02, f"+{spike_diff:.0f} spikes (+{sub['diff']:.0f}%)  (p={sub['p']})",
              transform=axs.transAxes, ha="right", va="bottom", fontsize=10.5, fontweight="bold",
              color=sub["color"])

    # --- bar chart: the "spike" itself, opposite vs preferred, same scale every row ---
    axb = fig.add_axes([BAR_X, y0 + 0.02, BAR_W, row_h - 0.04])
    bar_vals = [anti.mean(), pref.mean()]
    bar_colors = [sub["color"] + "55", sub["color"]]  # faded vs solid, same hue
    bars = axb.bar(["opp", "pref"], bar_vals, color=bar_colors, width=0.6, edgecolor="none")
    for b, v in zip(bars, bar_vals):
        axb.text(b.get_x() + b.get_width() / 2, v + GLOBAL_BAR_MAX * 0.03, f"{v:.0f}",
                  ha="center", va="bottom", fontsize=8.5)
    axb.set_ylim(0, GLOBAL_BAR_MAX)
    axb.spines[["top", "right"]].set_visible(False)
    axb.tick_params(axis="both", labelsize=8.5)
    if i == 0:
        axb.set_title("mean spikes", fontsize=9.5)

plt.savefig("images/cardinal_plate.png", dpi=150, bbox_inches="tight")
print("saved images/cardinal_plate.png")
