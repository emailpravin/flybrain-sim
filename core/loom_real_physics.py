"""
Real time-to-collision looming stimulus, built the way Card & Dickinson
2008 and the broader Gabbiani/Hatsopoulos LGMD literature actually define
it: purely in terms of angular size (degrees) and time (ms), not a fake
"zoom into a photo" trick.

Physics: for an object of half-size l approaching at speed v, angular size
    theta(t) = 2 * atan( tau / T(t) )
where tau = l/|v| (this project's "how fast is it approaching", expressible
as a real speed once a real object size is chosen -- see research_log.md)
and T(t) = time remaining until contact = tau/tan(theta_start/2) - t.

Instead of a fake image "zoom", this directly grows the RADIUS of driven
retina neurons each frame (like blob_looming_growing.py, avoiding its
zoom-crop brightness confound), with the radius at each frame computed
from the real theta(t) above, converted to this dataset's real
hex-unit-to-degree calibration (1 hex unit = 5.625 degrees, established
earlier this project from the LC11 8.8-degree size-tuning work).

Usage:
  python loom_real_physics.py blob_control.jpg mi1_columns.csv out.npy \
      --center-hex1 18 --center-hex2 20 \
      --tau-ms 50 --start-deg 3 --end-deg 120 --frame-interval-ms 5
"""
import argparse
import numpy as np
import pandas as pd
from PIL import Image
from scipy import ndimage

DEG_PER_HEX_UNIT = 5.625  # real, established this project (radius=4 units = 22.5 deg)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("photo")
    p.add_argument("columns_csv")
    p.add_argument("out_npy")
    p.add_argument("--center-hex1", type=float, required=True)
    p.add_argument("--center-hex2", type=float, required=True)
    p.add_argument("--tau-ms", type=float, required=True,
                    help="Real time-to-contact (l/|v|) in ms. Smaller = faster approach.")
    p.add_argument("--start-deg", type=float, default=3.0,
                    help="Starting angular size in degrees (real paper: 2-3 deg)")
    p.add_argument("--end-deg", type=float, default=120.0,
                    help="Final angular size in degrees (real paper: 120-130 deg, capped by "
                         "this dataset's real eye coverage)")
    p.add_argument("--frame-interval-ms", type=float, default=5.0)
    p.add_argument("--max-eye-radius", type=float, default=20.0,
                    help="Hard cap on hex-unit radius (this dataset's real eye extent)")
    args = p.parse_args()

    tau_s = args.tau_ms / 1000.0
    start_rad = np.radians(args.start_deg)
    end_rad = np.radians(args.end_deg)

    # T(t) = time remaining until contact; theta(t) = 2*atan(tau/T(t))
    # => T = tau / tan(theta/2)
    T_start = tau_s / np.tan(start_rad / 2)
    T_end = tau_s / np.tan(end_rad / 2)
    duration_s = T_start - T_end
    if duration_s <= 0:
        raise ValueError(f"start-deg >= end-deg makes no sense for a growing loom (T_start={T_start*1000:.1f}ms, T_end={T_end*1000:.1f}ms)")

    n_frames = max(2, int(round(duration_s * 1000 / args.frame_interval_ms)))
    print(f"tau={args.tau_ms}ms: real elapsed time from {args.start_deg} deg to {args.end_deg} deg "
          f"= {duration_s*1000:.1f}ms ({n_frames} frames @ {args.frame_interval_ms}ms)")

    cols = pd.read_csv(args.columns_csv)
    img = Image.open(args.photo).convert("L")
    arr = np.asarray(img, dtype=np.float32) / 255.0
    h, w = arr.shape
    bg = np.median(arr[0, :].tolist() + arr[-1, :].tolist() + arr[:, 0].tolist() + arr[:, -1].tolist())
    contrast = np.clip(bg - arr, 0, 1)
    contrast = ndimage.gaussian_filter(contrast, sigma=max(1, min(h, w) / 60))

    dist_all = np.hypot(cols["hex1"] - args.center_hex1, cols["hex2"] - args.center_hex2)
    all_ids = sorted(cols.loc[dist_all <= args.max_eye_radius, "bodyId"])
    idx = {b: i for i, b in enumerate(all_ids)}

    stack = np.zeros((n_frames, len(all_ids)), dtype=np.float32)
    frame_meta = []
    for f in range(n_frames):
        t_s = f * args.frame_interval_ms / 1000.0
        T_remaining = T_start - t_s
        theta_deg = 2 * np.degrees(np.arctan(tau_s / max(1e-6, T_remaining)))
        r_hex = min(args.max_eye_radius, theta_deg / DEG_PER_HEX_UNIT)

        win = cols[dist_all <= r_hex]
        if len(win) > 0:
            u = (win["hex1"] - (args.center_hex1 - r_hex)) / max(1e-6, 2 * r_hex)
            v = (win["hex2"] - (args.center_hex2 - r_hex)) / max(1e-6, 2 * r_hex)
            px = np.clip((u * (w - 1)).round().astype(int), 0, w - 1)
            py = np.clip((v * (h - 1)).round().astype(int), 0, h - 1)
            stim = contrast[py, px]
            for b, s in zip(win["bodyId"], stim):
                stack[f, idx[b]] = s

        frame_meta.append((f, t_s * 1000, theta_deg, r_hex, len(win)))

    np.save(args.out_npy, stack)
    pd.DataFrame({"bodyId": all_ids}).to_csv(args.out_npy.replace(".npy", "_bodyids.csv"), index=False)

    print(f"{'frame':>5} {'t_ms':>8} {'theta_deg':>10} {'r_hex':>7} {'n_neurons':>10}")
    for f, t_ms, theta_deg, r_hex, n in frame_meta:
        print(f"{f:>5} {t_ms:>8.1f} {theta_deg:>10.2f} {r_hex:>7.2f} {n:>10}")
    print(f"saved {stack.shape} to {args.out_npy}")


if __name__ == "__main__":
    main()
