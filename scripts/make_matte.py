#!/usr/bin/env python3
"""
Speaker matte generator (optional step).

Cuts the speaker (+ hands + brochure) out of every frame so that light trails, glows and
background grading can sit *behind* the presenter.  Uses BiRefNet-lite (MIT licence) through
onnxruntime on the CPU.  It is slow (a few seconds per frame) but resumable: frames that
already exist are skipped, and the work can be split between several processes.

    python3 scripts/make_matte.py --video assets/original/video.mov
    # split the work over two processes (each with 2 threads):
    python3 scripts/make_matte.py --video assets/original/video.mov --mod 4 --offsets 1,2 --threads 2 &
    python3 scripts/make_matte.py --video assets/original/video.mov --mod 4 --offsets 3,0 --threads 2 &

Output: assets/work/matte_raw/0001.png … (8-bit alpha, 540x960).  Run scripts/assemble_matte.py next.
"""
import argparse
import os
import subprocess
import sys
import time
import urllib.request

import numpy as np
from PIL import Image

MODEL_URL = "https://huggingface.co/onnx-community/BiRefNet_lite-ONNX/resolve/main/onnx/model.onnx"
MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
STD = np.array([0.229, 0.224, 0.225], dtype=np.float32)
W, H = 540, 960


def ensure_model(path):
    if os.path.exists(path):
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    print(f"downloading BiRefNet-lite model to {path} (224 MB) ...", flush=True)
    urllib.request.urlretrieve(MODEL_URL, path)


def extract_frames(video, frames_dir, fps):
    if os.path.isdir(frames_dir) and len(os.listdir(frames_dir)) > 0:
        return
    os.makedirs(frames_dir, exist_ok=True)
    subprocess.run(
        ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", video,
         "-vf", f"fps={fps},scale={W}:{H}:flags=lanczos", os.path.join(frames_dir, "%04d.png")],
        check=True,
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", default="assets/original/video.mov")
    ap.add_argument("--work", default="assets/work")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--threads", type=int, default=4)
    ap.add_argument("--mod", type=int, default=1, help="split frames into this many residue classes")
    ap.add_argument("--offsets", default="0", help="comma list of residues (mod --mod) this process handles, in order")
    ap.add_argument("--limit", type=int, default=0, help="stop after this many frames (re-run to continue; keeps memory bounded)")
    ap.add_argument("--only", default="", help="comma list of frame numbers to compute (overrides the order above)")
    args = ap.parse_args()

    import onnxruntime as ort

    model_path = os.path.join(args.work, "models", "birefnet_lite.onnx")
    frames_dir = os.path.join(args.work, "frames_540")
    out_dir = os.path.join(args.work, "matte_raw")
    ensure_model(model_path)
    extract_frames(args.video, frames_dir, args.fps)
    os.makedirs(out_dir, exist_ok=True)

    names = sorted(n for n in os.listdir(frames_dir) if n.endswith(".png"))
    total = len(names)
    offsets = [int(x) for x in args.offsets.split(",")]
    order = [i for off in offsets for i in range(1, total + 1) if i % args.mod == off % args.mod]
    if args.only:
        order = [int(x) for x in args.only.split(",")]
    todo = [i for i in order if not os.path.exists(os.path.join(out_dir, f"{i:04d}.png"))]
    if args.limit:
        todo = todo[: args.limit]
    print(f"{total} frames, {len(todo)} to do in this process", flush=True)

    so = ort.SessionOptions()
    so.intra_op_num_threads = args.threads
    # keep peak memory down: the default arena growth strategy can balloon past 10 GB at 1024x1024
    providers = [("CPUExecutionProvider", {"arena_extend_strategy": "kSameAsRequested"})]
    sess = ort.InferenceSession(model_path, so, providers=providers)
    in_name = sess.get_inputs()[0].name
    # hand the memory arena back to the OS after every frame (keeps the footprint far below the ~12 GB peak)
    run_opts = ort.RunOptions()
    run_opts.add_run_config_entry("memory.enable_memory_arena_shrinkage", "cpu:0")

    t0 = time.time()
    for n, i in enumerate(todo, 1):
        im = Image.open(os.path.join(frames_dir, f"{i:04d}.png")).convert("RGB")
        x = np.asarray(im.resize((1024, 1024), Image.BILINEAR), dtype=np.float32) / 255.0
        x = ((x - MEAN) / STD).transpose(2, 0, 1)[None].astype(np.float32)
        a = sess.run(None, {in_name: x}, run_options=run_opts)[-1][0, 0]
        if a.min() < 0 or a.max() > 1:  # logits -> probabilities
            a = 1.0 / (1.0 + np.exp(-a))
        a8 = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).resize(im.size, Image.BILINEAR)
        a8.save(os.path.join(out_dir, f"{i:04d}.png"))
        if n % 10 == 0 or n == len(todo):
            el = time.time() - t0
            print(f"  {n}/{len(todo)}  {el / n:.1f}s/frame  eta {(len(todo) - n) * el / n / 60:.1f} min", flush=True)


if __name__ == "__main__":
    sys.exit(main())
