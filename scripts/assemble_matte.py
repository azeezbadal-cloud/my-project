#!/usr/bin/env python3
"""
Turn raw per-frame mattes into public/fg.webm — the presenter on a transparent background.

    python3 scripts/assemble_matte.py                     # uses assets/work/matte_raw (BiRefNet)
    python3 scripts/assemble_matte.py --src assets/work/matte_dev --out public/fg_dev.webm

What it does
  * removes hanging ornaments / strings just above the head (clean_above_head),
  * fills frames that were not computed (interpolates between neighbours),
  * smooths the matte slightly over time to stop edge flicker,
  * "rescues" things the AI model missed – e.g. the brochure when it is held out to the side, detached from the body:
    anything that differs from the static wall (a median "clean plate" of the room) is added back,
  * mirrors it when the footage was mirrored (--flip 1, must match FLIP in prepare-footage.sh),
  * upsamples to 1080x1920, tightens + feathers the edge,
  * forces the desk strip at the very bottom to stay fully opaque (nothing interesting is "background" down there),
  * muxes it with public/footage.mp4 into a VP9 WebM with an alpha channel.
"""
import argparse
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageFilter

W, H = 1080, 1920


# ── fast binary morphology (square kernels, separable, O(pixels)) ─────────────────────────────
def _win_sum(a, k, axis, pad_val):
    r = k // 2
    pw = [(0, 0), (0, 0)]
    pw[axis] = (r, r)
    p = np.pad(a.astype(np.int32), pw, constant_values=pad_val)
    c = np.cumsum(p, axis=axis)
    zshape = list(c.shape)
    zshape[axis] = 1
    c = np.concatenate([np.zeros(zshape, dtype=c.dtype), c], axis=axis)
    n = a.shape[axis]
    hi = [slice(None), slice(None)]
    lo = [slice(None), slice(None)]
    hi[axis] = slice(k, k + n)
    lo[axis] = slice(0, n)
    return c[tuple(hi)] - c[tuple(lo)]


def erode(m, k):
    return _win_sum(_win_sum(m, k, 1, 1) == k, k, 0, 1) == k


def dilate(m, k):
    return _win_sum(_win_sum(m, k, 1, 0) > 0, k, 0, 0) > 0


def clean_above_head(a8):
    """Remove thin, detached bits (hanging ornaments, strings) just above the top of the head/body.

    The body is found with a morphological opening (kills anything thinner than ~13 px at 540x960); in a band
    above and just below the top of the body only pixels within a few px of that body are kept. Hair stays,
    detached beads/stalks go.  Everything lower in the frame is left untouched.
    """
    opened = dilate(erode(a8 > 128, 13), 13)
    rows = np.where(opened.sum(axis=1) >= 12)[0]
    if len(rows) == 0:
        return a8
    y0 = int(rows[0])
    allowed = np.asarray(
        Image.fromarray((dilate(opened, 11) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.5)), dtype=np.float32
    ) / 255.0
    yy = np.arange(a8.shape[0], dtype=np.float32)[:, None]
    w = np.clip((yy - (y0 + 10)) / 14.0, 0, 1)  # 0 above (top+10px) → cleaned, 1 below (top+24px) → original
    return (a8.astype(np.float32) * (allowed * (1 - w) + w)).astype(np.uint8)


def build_plate(frames_dir, n):
    """Median 'clean plate' of the room + a mask of where that plate is reliable (wall visible in most frames)."""
    idx = list(range(1, n + 1, 4))
    first = np.asarray(Image.open(os.path.join(frames_dir, f"{idx[0]:04d}.png")).convert("RGB"))
    h, w = first.shape[:2]
    stack = np.empty((len(idx), h, w, 3), dtype=np.uint8)
    for j, i in enumerate(idx):
        stack[j] = np.asarray(Image.open(os.path.join(frames_dir, f"{i:04d}.png")).convert("RGB"))
    plate = np.empty((h, w, 3), dtype=np.float32)
    stable = np.empty((h, w), dtype=bool)
    step = 96
    for r0 in range(0, h, step):
        blk = stack[:, r0 : r0 + step].astype(np.float32)
        med = np.median(blk, axis=0)
        plate[r0 : r0 + step] = med
        dist = np.sqrt(((blk - med) ** 2).sum(-1))
        stable[r0 : r0 + step] = (dist < 35).mean(0) > 0.62
    return plate, erode(stable, 9)


def rescue(alpha8, rgb, plate, stable):
    """Add back anything that differs from the static wall but the model left out (e.g. a detached brochure).

    Safeguards: camera exposure drift is compensated (this is what avoids false detections), the desk strip is
    ignored, specks are removed and implausibly large detections (a global change of the picture) are discarded.
    """
    f = rgb.astype(np.float32)
    # exposure compensation: gain of this frame relative to the clean plate, measured on the reliable wall
    gain = np.median(f[stable] / (plate[stable] + 1.0), axis=0) if stable.any() else np.ones(3, dtype=np.float32)
    d = np.sqrt(((f / np.clip(gain, 0.6, 1.6) - plate) ** 2).sum(-1))
    miss = (d > 48) & stable & (alpha8 < 90)
    miss[int(0.86 * miss.shape[0]) :] = False  # not the desk strip
    miss = dilate(erode(miss, 17), 17)  # drop specks (opening)
    miss = erode(dilate(miss, 15), 15)  # fill small holes, e.g. photos printed on the brochure (closing)
    if not miss.any():
        return alpha8, 0
    miss = dilate(miss, 5)
    if not miss.any() or miss.mean() > 0.06:
        return alpha8, 0
    soft = np.asarray(Image.fromarray((miss * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2)))
    return np.maximum(alpha8, soft), int(miss.sum())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="assets/work/matte_raw")
    ap.add_argument("--footage", default="public/footage.mp4")
    ap.add_argument("--out", default="public/fg.webm")
    ap.add_argument("--frames-dir", default="assets/work/frames_540", help="540x960 RGB frames (made by make_matte.py)")
    ap.add_argument("--rescue", type=int, default=1, help="1 = add back objects the model missed (needs --frames-dir)")
    ap.add_argument("--flip", type=int, default=1)
    ap.add_argument("--frames", type=int, default=0, help="number of frames in the footage (default: read from --footage)")
    ap.add_argument("--solid-from", type=float, default=0.85, help="height fraction where 'always opaque' starts fading in (the desk strip)")
    ap.add_argument("--solid-full", type=float, default=0.91, help="height fraction where it is fully opaque")
    ap.add_argument("--crf", type=int, default=14)
    args = ap.parse_args()

    n = args.frames
    if not n:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=nb_frames", "-of", "csv=p=0", args.footage],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        n = int(out)
    have = {}
    for name in os.listdir(args.src):
        if name.endswith(".png"):
            have[int(name[:-4])] = os.path.join(args.src, name)
    if not have:
        sys.exit(f"no mattes found in {args.src}")
    idx = sorted(have)
    print(f"{len(have)}/{n} mattes available ({len(have) * 100 // n}%) – missing frames are interpolated", flush=True)

    first = np.asarray(Image.open(have[idx[0]]).convert("L"))
    h0, w0 = first.shape
    seq = np.zeros((n, h0, w0), dtype=np.uint8)
    for i in range(1, n + 1):
        if i in have:
            seq[i - 1] = clean_above_head(np.asarray(Image.open(have[i]).convert("L")))
    # interpolate the gaps
    for i in range(1, n + 1):
        if i in have:
            continue
        prev = max((k for k in idx if k < i), default=None)
        nxt = min((k for k in idx if k > i), default=None)
        if prev is None:
            seq[i - 1] = seq[nxt - 1]
        elif nxt is None:
            seq[i - 1] = seq[prev - 1]
        else:
            w = (i - prev) / (nxt - prev)
            seq[i - 1] = ((1 - w) * seq[prev - 1].astype(np.float32) + w * seq[nxt - 1].astype(np.float32)).astype(np.uint8)

    # light temporal smoothing
    sm = np.empty_like(seq)
    for i in range(n):
        a = seq[max(i - 1, 0)].astype(np.float32)
        b = seq[i].astype(np.float32)
        c = seq[min(i + 1, n - 1)].astype(np.float32)
        sm[i] = (0.2 * a + 0.6 * b + 0.2 * c).astype(np.uint8)

    plate = stable = None
    if args.rescue and os.path.isdir(args.frames_dir) and len(os.listdir(args.frames_dir)) >= n:
        print("building clean plate of the room …", flush=True)
        plate, stable = build_plate(args.frames_dir, n)
    elif args.rescue:
        print("note: no frames dir – skipping the 'rescue missed objects' step", flush=True)

    yy = np.linspace(0, 1, H, dtype=np.float32)[:, None]
    solid = np.clip((yy - args.solid_from) / max(args.solid_full - args.solid_from, 1e-3), 0, 1)

    cmd = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-f", "rawvideo", "-pix_fmt", "gray", "-s", f"{W}x{H}", "-r", "30", "-i", "pipe:0",
        "-i", args.footage,
        "-filter_complex", "[1:v][0:v]alphamerge,format=yuva420p[v]",
        "-map", "[v]", "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-b:v", "0", "-crf", str(args.crf),
        "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
        "-deadline", "good", "-cpu-used", "4", "-row-mt", "1", "-auto-alt-ref", "0", "-an", "-shortest", args.out,
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    rescued = []
    for i in range(n):
        a8 = sm[i]
        if plate is not None:
            rgb = np.asarray(Image.open(os.path.join(args.frames_dir, f"{i + 1:04d}.png")).convert("RGB"))
            a8, px = rescue(a8, rgb, plate, stable)
            if px:
                rescued.append((i + 1, px))
        img = Image.fromarray(a8).resize((W, H), Image.BICUBIC)
        if args.flip:
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
        a = np.asarray(img, dtype=np.float32) / 255.0
        a = np.clip((a - 0.5) * 1.5 + 0.5, 0, 1)  # tighten the edge a little
        img = Image.fromarray((a * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))
        a = np.asarray(img, dtype=np.float32) / 255.0
        a = np.maximum(a, solid)
        proc.stdin.write((a * 255 + 0.5).astype(np.uint8).tobytes())
        if (i + 1) % 100 == 0:
            print(f"  {i + 1}/{n}", flush=True)
    proc.stdin.close()
    rc = proc.wait()
    if rc != 0:
        sys.exit(f"ffmpeg failed ({rc})")
    if rescued:
        print(f"rescued missed objects in {len(rescued)} frames: {[f for f, _ in rescued]}")
    print("wrote", args.out)


if __name__ == "__main__":
    main()
