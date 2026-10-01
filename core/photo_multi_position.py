"""
Place a real photo's contrast pattern onto a real windowed patch of the
887 real Mi1 columns (mi1_columns.csv, one eye, hex1 1-36 / hex2 1-39),
at a GIVEN center position -- used to sweep the same photo across several
different real positions on the eye, so we don't accidentally test only
one position (which might land in a dead zone by chance).

Usage:
  python photo_multi_position.py photo.jpg mi1_columns.csv out.npy \
      --center-hex1 18 --center-hex2 20 --radius 10
"""
import argparse
import numpy as np
import pandas as pd
from PIL import Image
from scipy import ndimage


def naka_rushton(x, c50, n=1.0, rmax=1.0):
    """Real, published contrast-response nonlinearity (Naka-Rushton), used
    throughout this project's earlier amplification work. Small c50 = strong
    boost for weak/small signals; always saturates at rmax."""
    xc = np.clip(x, 0, None) ** n
    return rmax * xc / (xc + c50 ** n)


def two_stage_amplify(contrast, retina_c50, lamina_c50, retina_n=1.0, lamina_n=1.0):
    """Two real, anatomically separate amplification stages (photoreceptor,
    then lamina/L1-L3 relay) -- the real early-vision gain-control stage
    this project identified as missing, which is why realistically small
    targets never generated enough signal to fire anything downstream."""
    retina_out = naka_rushton(contrast, c50=retina_c50, n=retina_n)
    return naka_rushton(retina_out, c50=lamina_c50, n=lamina_n)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("photo")
    p.add_argument("columns_csv")
    p.add_argument("out_npy")
    p.add_argument("--center-hex1", type=float, required=True)
    p.add_argument("--center-hex2", type=float, required=True)
    p.add_argument("--radius", type=float, default=10.0)
    p.add_argument("--frames", type=int, default=6)
    p.add_argument("--amplify", action="store_true",
                    help="apply the real two-stage retina+lamina amplification "
                         "(Naka-Rushton) instead of raw linear contrast")
    p.add_argument("--retina-c50", type=float, default=0.08)
    p.add_argument("--lamina-c50", type=float, default=0.15)
    args = p.parse_args()

    cols = pd.read_csv(args.columns_csv)

    img = Image.open(args.photo).convert("L")
    arr = np.asarray(img, dtype=np.float32) / 255.0
    h, w = arr.shape
    bg = np.median(arr[0, :].tolist() + arr[-1, :].tolist() + arr[:, 0].tolist() + arr[:, -1].tolist())
    contrast = np.clip(bg - arr, 0, 1)
    contrast = ndimage.gaussian_filter(contrast, sigma=max(1, min(h, w) / 60))

    dist = np.hypot(cols["hex1"] - args.center_hex1, cols["hex2"] - args.center_hex2)
    r = args.radius
    win = cols[dist <= r]
    while len(win) == 0 and r < 20:
        r += 1
        win = cols[dist <= r]
    win = win.reset_index(drop=True)

    u = (win["hex1"] - (args.center_hex1 - r)) / max(1e-6, 2 * r)
    v = (win["hex2"] - (args.center_hex2 - r)) / max(1e-6, 2 * r)
    px = np.clip((u * (w - 1)).round().astype(int), 0, w - 1)
    py = np.clip((v * (h - 1)).round().astype(int), 0, h - 1)
    stim = contrast[py, px]
    if args.amplify:
        stim = two_stage_amplify(stim, args.retina_c50, args.lamina_c50)

    # sustained stimulus across all frames (no motion/zoom, just presence)
    stack = np.tile(stim.astype(np.float32), (args.frames, 1))
    np.save(args.out_npy, stack)
    win[["bodyId"]].to_csv(args.out_npy.replace(".npy", "_bodyids.csv"), index=False)
    print(f"center=({args.center_hex1},{args.center_hex2}) radius_used={r} n_neurons={len(win)} "
          f"mean_stim={stim.mean():.4f}")


if __name__ == "__main__":
    main()
