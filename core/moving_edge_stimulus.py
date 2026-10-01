"""
A small, localized dark object translating steadily across the retina --
built specifically to match Tm2's real, literature-documented preference
(Behnia/Clark 2014 and follow-ups): a LOCAL dark edge/OFF stimulus with
an antagonistic surround, not a large synchronized region darkening at
once (which is what the earlier loom and sweep tests both were, and
which likely triggered Tm2's surround suppression instead of exciting
its center).

Unlike image_to_retina_sequence.py's "sweep" mode (which shifts the
WHOLE image and drives the whole eye every frame), this drives only a
SMALL window of neurons at each frame, moving frame to frame -- a
genuinely local moving dot/edge, not a whole-field shift.

Usage:
  python moving_edge_stimulus.py blob_control.jpg mi1_columns.csv out.npy \
      --start-hex1 8 --end-hex1 28 --hex2 20 --radius 1.0 --frames 60 --frame-interval-ms 10
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
    p.add_argument("--start-hex1", type=float, required=True)
    p.add_argument("--end-hex1", type=float, required=True)
    p.add_argument("--hex2", type=float, required=True, help="fixed hex2 (straight horizontal path)")
    p.add_argument("--radius", type=float, default=1.0, help="small, local window radius in hex units")
    p.add_argument("--frames", type=int, default=60)
    p.add_argument("--frame-interval-ms", type=float, default=10.0)
    args = p.parse_args()

    cols = pd.read_csv(args.columns_csv)
    img = Image.open(args.photo).convert("L")
    arr = np.asarray(img, dtype=np.float32) / 255.0
    h, w = arr.shape
    bg = np.median(arr[0, :].tolist() + arr[-1, :].tolist() + arr[:, 0].tolist() + arr[:, -1].tolist())
    contrast = np.clip(bg - arr, 0, 1)
    contrast = ndimage.gaussian_filter(contrast, sigma=max(1, min(h, w) / 60))

    positions = np.linspace(args.start_hex1, args.end_hex1, args.frames)

    # union of all neurons ever touched, so the output array has a fixed neuron set
    r = args.radius
    dist_union = np.hypot(cols["hex1"] - (args.start_hex1 + args.end_hex1) / 2, cols["hex2"] - args.hex2)
    max_span = abs(args.end_hex1 - args.start_hex1) / 2 + r
    union = cols[dist_union <= max_span].reset_index(drop=True)
    all_ids = sorted(union["bodyId"])
    idx = {b: i for i, b in enumerate(all_ids)}

    stack = np.zeros((args.frames, len(all_ids)), dtype=np.float32)
    speed_deg_per_s = abs(args.end_hex1 - args.start_hex1) * 5.625 / (args.frames * args.frame_interval_ms / 1000.0)
    print(f"Object radius={r} hex units ({r*5.625:.1f} deg), path length={abs(args.end_hex1-args.start_hex1)} hex units, "
          f"speed={speed_deg_per_s:.1f} deg/s")

    for f, center_hex1 in enumerate(positions):
        dist = np.hypot(cols["hex1"] - center_hex1, cols["hex2"] - args.hex2)
        win = cols[dist <= r]
        if len(win) == 0:
            continue
        u = (win["hex1"] - (center_hex1 - r)) / max(1e-6, 2 * r)
        v = (win["hex2"] - (args.hex2 - r)) / max(1e-6, 2 * r)
        px = np.clip((u * (w - 1)).round().astype(int), 0, w - 1)
        py = np.clip((v * (h - 1)).round().astype(int), 0, h - 1)
        stim = contrast[py, px]
        for b, s in zip(win["bodyId"], stim):
            if b in idx:
                stack[f, idx[b]] = s
        print(f"  frame {f}: center_hex1={center_hex1:.2f}, n_neurons_active={len(win)}, mean_stim={stim.mean():.3f}")

    np.save(args.out_npy, stack)
    pd.DataFrame({"bodyId": all_ids}).to_csv(args.out_npy.replace(".npy", "_bodyids.csv"), index=False)
    print(f"saved {stack.shape} to {args.out_npy} (total driven neurons: {len(all_ids)})")


if __name__ == "__main__":
    main()
