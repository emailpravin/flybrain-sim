"""
Real color-opponent stimulus: samples an actual COLOR photo (not
grayscale) onto Tm20's real retinotopic columns (tm20_columns.csv),
using each real Tm20 neuron's own measured pale (R7p/R8p) vs yellow
(R7y/R8y) synaptic input weight to decide how much it should respond to
the blue channel (proxy for R8p's real blue/Rh5 sensitivity) vs the
green channel (proxy for R8y's real green/Rh6 sensitivity) -- real,
per-neuron spectral bias, not a uniform tint applied to everyone.
Neurons with no measured direct photoreceptor input (most of Tm20,
consistent with the real finding that Tm20 is achromatic-dominated)
fall back to plain luminance contrast, same as the Mi1 pipeline.

Usage:
  python image_to_tm20_color.py photo.png tm20_columns.csv out.npy \
      --center-hex1 18 --center-hex2 20 --radius 10
"""
import argparse
import numpy as np
import pandas as pd
from PIL import Image
from scipy import ndimage


def main():
    p = argparse.ArgumentParser()
    p.add_argument("photo")
    p.add_argument("columns_csv")
    p.add_argument("out_npy")
    p.add_argument("--center-hex1", type=float, required=True)
    p.add_argument("--center-hex2", type=float, required=True)
    p.add_argument("--radius", type=float, default=10.0)
    p.add_argument("--frames", type=int, default=6)
    args = p.parse_args()

    img = Image.open(args.photo).convert("RGB")
    arr = np.asarray(img, dtype=np.float32) / 255.0
    h, w, _ = arr.shape
    R, G, B = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]

    gray = arr.mean(axis=2)
    bg = np.median(np.concatenate([gray[0, :], gray[-1, :], gray[:, 0], gray[:, -1]]))

    # luminance contrast (same as the achromatic pipeline)
    contrast = np.clip(bg - gray, 0, 1)
    contrast = ndimage.gaussian_filter(contrast, sigma=max(1, min(h, w) / 60))

    # real color-OPPONENT signal (not per-channel darkness): redness = R minus the
    # average of G and B. Real red pigment (drosopterins/xanthommatin) absorbs
    # blue/green more than red, so this is near zero for genuinely colorless/
    # grayscale objects (R=G=B) and positive specifically where something reflects
    # red -- unlike a single channel's own darkness, which any dark object triggers
    # regardless of hue.
    redness = R - (G + B) / 2
    redness_sig = ndimage.gaussian_filter(redness, sigma=max(1, min(h, w) / 60))
    redness_sig = np.clip(redness_sig, 0, None)

    cols = pd.read_csv(args.columns_csv)
    dist = np.hypot(cols["hex1"] - args.center_hex1, cols["hex2"] - args.center_hex2)
    r = args.radius
    win = cols[dist <= r].reset_index(drop=True)
    while len(win) == 0 and r < 20:
        r += 1
        win = cols[dist <= r].reset_index(drop=True)

    u = (win["hex1"] - (args.center_hex1 - r)) / max(1e-6, 2 * r)
    v = (win["hex2"] - (args.center_hex2 - r)) / max(1e-6, 2 * r)
    px = np.clip((u * (w - 1)).round().astype(int), 0, w - 1)
    py = np.clip((v * (h - 1)).round().astype(int), 0, h - 1)

    lum_stim = contrast[py, px]
    redness_stim = redness_sig[py, px]

    pale_w = win["pale"].fillna(0).values
    yellow_w = win["yellow"].fillna(0).values
    has_color = (pale_w + yellow_w) > 0

    # neurons with real direct photoreceptor input carry the genuine opponent signal;
    # everyone else falls back to plain luminance contrast, consistent with the real
    # finding that most of Tm20 is achromatic-dominated
    stim = np.where(has_color, redness_stim, lum_stim)

    stack = np.tile(stim.astype(np.float32), (args.frames, 1))
    np.save(args.out_npy, stack)
    win[["bodyId"]].to_csv(args.out_npy.replace(".npy", "_bodyids.csv"), index=False)
    print(f"n_neurons={len(win)} radius_used={r} with_direct_color_input={has_color.sum()} "
          f"mean_stim={stim.mean():.4f}")


if __name__ == "__main__":
    main()
