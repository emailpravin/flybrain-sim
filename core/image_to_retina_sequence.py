"""
Generate a multi-frame "approach" sequence from a single static image by
progressively zooming in on the subject's centroid (simulating it getting
closer over time), then sample each frame onto the fly's real visual-column
grid (Mi1 neurons) -- producing genuine frame-to-frame CHANGE, which is what
real motion-detector neurons (T4/T5) require and a single static image
cannot provide.

This is a simplification: real approach motion is smooth and continuous;
this produces discrete frames at a fixed step. It's a legitimate proxy for
"getting closer over time" but not a physically exact optic-flow simulation.

Usage:
  python image_to_retina_sequence.py photo_bw.jpg mi1_columns.csv out_stimulus.npy \\
      --frames 6 --zoom-per-frame 1.15
"""
import argparse

import numpy as np
import pandas as pd
from PIL import Image
from scipy import ndimage


def zoom_frame(arr, zoom_factor):
    h, w = arr.shape
    ch, cw = h / 2, w / 2
    new_h, new_w = h / zoom_factor, w / zoom_factor
    y0, y1 = int(ch - new_h / 2), int(ch + new_h / 2)
    x0, x1 = int(cw - new_w / 2), int(cw + new_w / 2)
    cropped = arr[max(0, y0):min(h, y1), max(0, x0):min(w, x1)]
    zoomed = ndimage.zoom(cropped, (h / cropped.shape[0], w / cropped.shape[1]), order=1)
    return zoomed


def oscillate_frame(arr, shift_frac, bg_level):
    """Shift the image horizontally by shift_frac of its width, padding with background."""
    h, w = arr.shape
    shift_px = int(round(shift_frac * w))
    shifted = np.full_like(arr, bg_level)
    if shift_px >= 0:
        shifted[:, shift_px:] = arr[:, :w - shift_px] if shift_px < w else bg_level
    else:
        s = -shift_px
        shifted[:, :w - s] = arr[:, s:]
    return shifted


def sample_onto_columns(contrast_map, columns):
    h, w = contrast_map.shape
    h1min, h1max = columns["hex1"].min(), columns["hex1"].max()
    h2min, h2max = columns["hex2"].min(), columns["hex2"].max()
    u = (columns["hex1"] - h1min) / (h1max - h1min + 1e-9)
    v = (columns["hex2"] - h2min) / (h2max - h2min + 1e-9)
    px = np.clip((u * (w - 1)).round().astype(int), 0, w - 1)
    py = np.clip((v * (h - 1)).round().astype(int), 0, h - 1)
    return contrast_map[py, px]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("photo")
    parser.add_argument("columns_csv")
    parser.add_argument("out_npy")
    parser.add_argument("--frames", type=int, default=6)
    parser.add_argument("--zoom-per-frame", type=float, default=1.15,
                         help="Multiplicative zoom applied each frame (>1 = getting closer)")
    parser.add_argument("--mode", choices=["zoom", "oscillate", "sweep", "loom"], default="zoom")
    parser.add_argument("--oscillate-amplitude", type=float, default=0.15,
                         help="Max horizontal shift as a fraction of image width (oscillate mode)")
    parser.add_argument("--frame-interval-ms", type=float, default=10.0,
                         help="Real time between frames in ms (loom mode). Needs to be short "
                              "relative to Giant Fiber first-spike latency (~20ms) or 'speed' "
                              "differences arrive too late to affect the decisive first spike.")
    parser.add_argument("--tau-ms", type=float, default=400.0,
                         help="Time-to-contact in ms (loom mode). SMALLER = faster/more imminent "
                              "approach. This is the real looming-stimulus parameterization used in "
                              "Gabbiani/Hatsopoulos LGMD and Drosophila GF literature (object "
                              "angular size ~ 1/(tau - t)), not an arbitrary per-frame multiplier -- "
                              "unlike --mode zoom, the expansion RATE (not just final size) differs "
                              "by tau starting from frame 0.")
    parser.add_argument("--max-zoom", type=float, default=6.0,
                         help="Cap on zoom factor (loom mode) to avoid blow-up near t=tau")
    args = parser.parse_args()

    img = Image.open(args.photo).convert("L")
    arr = np.asarray(img, dtype=np.float32) / 255.0
    h, w = arr.shape
    bg_level = np.median(arr[0, :].tolist() + arr[-1, :].tolist() + arr[:, 0].tolist() + arr[:, -1].tolist())

    columns = pd.read_csv(args.columns_csv)

    frame_stimuli = []
    for f in range(args.frames):
        if args.mode == "zoom":
            zoom = args.zoom_per_frame ** f
            frame_arr = zoom_frame(arr, zoom) if zoom > 1.0 else arr
            label = f"zoom={zoom:.2f}x"
        elif args.mode == "oscillate":
            phase = 2 * np.pi * f / max(1, args.frames - 1)
            shift_frac = args.oscillate_amplitude * np.sin(phase)
            frame_arr = oscillate_frame(arr, shift_frac, bg_level)
            label = f"shift={shift_frac:+.3f}"
        elif args.mode == "sweep":  # single-direction crossing, not back-and-forth
            t = f / max(1, args.frames - 1)
            shift_frac = -args.oscillate_amplitude + 2 * args.oscillate_amplitude * t
            frame_arr = oscillate_frame(arr, shift_frac, bg_level)
            label = f"sweep shift={shift_frac:+.3f}"
        else:  # loom: real time-to-contact angular-expansion physics, zoom(t) = 1/(1 - t/tau)
            t_ms = f * args.frame_interval_ms
            zoom = min(args.max_zoom, 1.0 / max(1e-3, 1.0 - t_ms / args.tau_ms))
            frame_arr = zoom_frame(arr, zoom) if zoom > 1.0 else arr
            label = f"t={t_ms:.0f}ms, zoom={zoom:.3f}x (tau={args.tau_ms:.0f}ms)"

        contrast_map = np.clip(bg_level - frame_arr, 0, 1)
        contrast_map = ndimage.gaussian_filter(contrast_map, sigma=max(1, min(h, w) / 80))
        stim = sample_onto_columns(contrast_map, columns)
        frame_stimuli.append(stim)
        print(f"  frame {f}: {label}, mean stimulus={stim.mean():.3f}, "
              f"columns with signal (>0.1)={np.sum(stim > 0.1)}")

    stack = np.stack(frame_stimuli, axis=0)  # (n_frames, n_columns)
    np.save(args.out_npy, stack)

    bodyids_path = args.out_npy.replace(".npy", "_bodyids.csv")
    columns[["bodyId"]].to_csv(bodyids_path, index=False)

    print(f"Saved stimulus sequence {stack.shape} to {args.out_npy}")
    print(f"Saved column bodyId order to {bodyids_path}")


if __name__ == "__main__":
    main()
