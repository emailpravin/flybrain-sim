"""
Real looming stimulus built WITHOUT the zoom-crop brightness confound
found earlier in this project: instead of cropping progressively
tighter into a photo (which artificially brightens the frame as it
crops), this GROWS the real window of driven Mi1 columns over frames,
using the SAME fixed-brightness blob image each time (blob_control.jpg,
a plain max-contrast black circle). More of the eye gets recruited each
frame, matching a real object getting bigger in the visual field, with
no brightness-per-pixel change at all -- the confound this project
documented cannot occur here.

Usage:
  python blob_looming_growing.py blob_control.jpg mi1_columns.csv out.npy \
      --center-hex1 18 --center-hex2 20 --radii 4,6,8,10,10,10
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
    p.add_argument("--radii", required=True, help="comma-separated radius per frame, e.g. 4,6,8,10,10,10")
    args = p.parse_args()

    radii = [float(r) for r in args.radii.split(",")]
    cols = pd.read_csv(args.columns_csv)

    img = Image.open(args.photo).convert("L")
    arr = np.asarray(img, dtype=np.float32) / 255.0
    h, w = arr.shape
    bg = np.median(arr[0, :].tolist() + arr[-1, :].tolist() + arr[:, 0].tolist() + arr[:, -1].tolist())
    contrast = np.clip(bg - arr, 0, 1)
    contrast = ndimage.gaussian_filter(contrast, sigma=max(1, min(h, w) / 60))

    max_r = max(radii)
    dist = np.hypot(cols["hex1"] - args.center_hex1, cols["hex2"] - args.center_hex2)
    union = cols[dist <= max_r].reset_index(drop=True)
    all_ids = sorted(union["bodyId"])
    idx = {b: i for i, b in enumerate(all_ids)}

    stack = np.zeros((len(radii), len(all_ids)), dtype=np.float32)
    for f, r in enumerate(radii):
        win = cols[dist <= r]
        u = (win["hex1"] - (args.center_hex1 - r)) / max(1e-6, 2 * r)
        v = (win["hex2"] - (args.center_hex2 - r)) / max(1e-6, 2 * r)
        px = np.clip((u * (w - 1)).round().astype(int), 0, w - 1)
        py = np.clip((v * (h - 1)).round().astype(int), 0, h - 1)
        stim = contrast[py, px]
        for b, s in zip(win["bodyId"], stim):
            stack[f, idx[b]] = s
        print(f"  frame {f}: radius={r} n_neurons={len(win)} mean_stim_over_driven={stim.mean():.3f} "
              f"mean_stim_over_full_window={stack[f].mean():.4f}")

    np.save(args.out_npy, stack)
    pd.DataFrame({"bodyId": all_ids}).to_csv(args.out_npy.replace(".npy", "_bodyids.csv"), index=False)
    print(f"saved {stack.shape} to {args.out_npy}")


if __name__ == "__main__":
    main()
