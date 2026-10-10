"""Plate: one shared retinal-progression diagram (the blob filling the
fly's eye) precisely aligned, by degree, with three trigger-angle
distributions below -- same x-axis (degrees) used throughout, eye-view
circles placed at their true horizontal position on that axis."""
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

DEG_PER_HEX_UNIT = 5.625
CENTER = (18.0, 20.0)
MAX_RADIUS_HEX = 20.0

cols = pd.read_csv("../../core/mi1_columns.csv")
dist = np.hypot(cols["hex1"] - CENTER[0], cols["hex2"] - CENTER[1])
eye = cols[dist <= MAX_RADIUS_HEX].copy()
eye["dist"] = dist[dist <= MAX_RADIUS_HEX]

with open("/tmp/plate_data.json") as f:
    data = json.load(f)

panels = [
    {"label": "1. Escape circuit\nalone (Blog 1)", "tag": "Baseline", "angles": data["p1"]},
    {"label": "2. Escape circuit\n+ octopamine (Blog 2)", "tag": "Excitatory (boost)", "angles": data["p2"]},
    {"label": "3. Escape circuit\n+ Li28 forced active\n(Blog 3, this post)", "tag": "Inhibitory (brake)", "angles": data["p3"]},
]
for p in panels:
    p["mean"] = float(np.mean(p["angles"]))
    p["std"] = float(np.std(p["angles"]))

checkpoints = [3, 15, 30, 45, 60, 75, 90, 112]
GLOBAL_XLIM = (0, 118)
LEFT, RIGHT = 0.17, 0.98

fig = plt.figure(figsize=(17, 9.3))

# --- shared reference axes for the eye-view row (defines the x<->figure mapping) ---
ax_top = fig.add_axes([LEFT, 0.70, RIGHT - LEFT, 0.26])
ax_top.set_xlim(*GLOBAL_XLIM)
ax_top.set_ylim(0, 1)
ax_top.axis("off")
fig.text(0.5, 0.975, "the blob filling the fly's eye (same progression, all conditions)",
          ha="center", fontsize=18, fontweight="bold")

circ_w_in, circ_h_in = 1.5, 1.5
fig_w_in, fig_h_in = fig.get_size_inches()
w_frac, h_frac = circ_w_in / fig_w_in, circ_h_in / fig_h_in

for deg in checkpoints:
    fx, _ = ax_top.transData.transform((deg, 0.5))
    fx_frac = fig.transFigure.inverted().transform((fx, 0))[0]
    ax_e = fig.add_axes([fx_frac - w_frac / 2, 0.715, w_frac, h_frac])
    r_hex = min(MAX_RADIUS_HEX, deg / DEG_PER_HEX_UNIT)
    lit = eye["dist"] <= r_hex
    ax_e.scatter(eye.loc[~lit, "hex1"], eye.loc[~lit, "hex2"], s=5, c="lightgray", edgecolors="none")
    ax_e.scatter(eye.loc[lit, "hex1"], eye.loc[lit, "hex2"], s=5, c="black", edgecolors="none")
    ax_e.add_patch(Circle(CENTER, MAX_RADIUS_HEX, fill=False, edgecolor="gray", linewidth=0.8))
    ax_e.set_xlim(CENTER[0] - MAX_RADIUS_HEX - 1, CENTER[0] + MAX_RADIUS_HEX + 1)
    ax_e.set_ylim(CENTER[1] - MAX_RADIUS_HEX - 1, CENTER[1] + MAX_RADIUS_HEX + 1)
    ax_e.set_aspect("equal")
    ax_e.axis("off")
    ax_e.text(0.5, -0.08, f"~{deg}deg", transform=ax_e.transAxes, ha="center", va="top", fontsize=10)

# vertical guide ticks on ax_top at each checkpoint, down through the whole figure
for deg in checkpoints:
    ax_top.axvline(deg, ymin=-0.05, ymax=0, color="#cccccc", linewidth=0.8, clip_on=False)

# --- three distribution rows, same x-axis, same left/right as ax_top ---
row_h = 0.14
row_gap = 0.055
top_y = 0.56
for pi, panel in enumerate(panels):
    y0 = top_y - pi * (row_h + row_gap) - row_h
    ax = fig.add_axes([LEFT, y0, RIGHT - LEFT, row_h])
    angles = panel["angles"]
    rng = np.random.default_rng(0)
    y_jitter = rng.uniform(-0.18, 0.18, size=len(angles))
    ax.scatter(angles, 0.3 + y_jitter, s=11, c="#1e73e8", alpha=0.75, edgecolors="none", zorder=3)
    ax.errorbar([panel["mean"]], [0.8], xerr=[panel["std"]], fmt="D", color="#0050d0",
                markersize=7, capsize=4, linewidth=1.4, markeredgewidth=0, zorder=4)
    ax.text(panel["mean"], 1.0, f"{panel['mean']:.1f}deg +/- {panel['std']:.1f}deg",
            ha="center", va="bottom", fontsize=10, color="#0050d0", fontweight="bold")
    ax.set_xlim(*GLOBAL_XLIM)
    ax.set_ylim(0, 1.25)
    ax.set_yticks([])
    for deg in checkpoints:
        ax.axvline(deg, color="#eeeeee", linewidth=0.8, zorder=0)
    ax.spines[["top", "right", "left"]].set_visible(False)
    if pi == len(panels) - 1:
        ax.set_xticks(checkpoints)
        ax.set_xlabel("degrees of the eye patch covered when the circuit fires (N=30 each)", fontsize=14)
        ax.tick_params(axis="x", labelsize=11)
    else:
        ax.set_xticks(checkpoints)
        ax.set_xticklabels([])
    ax.text(-0.17, 0.62, panel["label"], transform=ax.transAxes, ha="left", va="center",
            fontsize=11, fontweight="bold")
    ax.text(-0.17, 0.30, panel["tag"].upper(), transform=ax.transAxes, ha="left", va="center",
            fontsize=14, style="italic", fontweight="bold", color="#444444")

plt.savefig("three_panel_plate.png", dpi=150, bbox_inches="tight")
print("saved three_panel_plate.png")
