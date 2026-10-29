#!/usr/bin/env bash
# Conform + grade the original footage for the Remotion composition.
#
#   bash scripts/prepare-footage.sh [path/to/original.mov]
#
# Output:
#   public/footage.mp4         1080x1920, 30 fps constant, all-intra (frame-accurate seeking), graded
#   assets/work/voice_raw.wav  the untouched voice track (48 kHz stereo) for the audio mix
#
# Options (environment variables):
#   FLIP=1   mirror the picture horizontally (default). Selfie-camera footage is usually saved mirrored,
#            which makes the brochure / wall posters read backwards. Use FLIP=0 to keep it exactly as shot.
#   GRADE="..."  override the FFmpeg colour-grade filter chain below.
set -euo pipefail

IN="${1:-assets/original/video.mov}"
OUT="public/footage.mp4"
FLIP="${FLIP:-1}"

# Gentle professional grade: neutralise the yellow office cast, add a soft S-curve and a touch of clarity.
DEFAULT_GRADE="colorbalance=rs=-0.02:rm=-0.05:rh=-0.04:bs=0.04:bm=0.08:bh=0.08,\
eq=contrast=1.07:brightness=-0.012:saturation=1.06:gamma=0.98,\
curves=m='0/0 0.10/0.075 0.50/0.50 0.90/0.93 1/1',\
unsharp=5:5:0.45:5:5:0"
GRADE="${GRADE:-$DEFAULT_GRADE}"

FLIPF=""
if [ "$FLIP" = "1" ]; then FLIPF="hflip,"; fi

mkdir -p public assets/work
ffmpeg -y -hide_banner -loglevel error -i "$IN" -map 0:v:0 \
  -vf "${FLIPF}fps=30,scale=1080:1920:flags=lanczos,${GRADE},format=yuv420p" \
  -c:v libx264 -preset slow -crf 12 -g 1 -pix_fmt yuv420p \
  -color_primaries bt709 -color_trc bt709 -colorspace bt709 -an "$OUT"

ffmpeg -y -hide_banner -loglevel error -i "$IN" -vn -ac 2 -ar 48000 -c:a pcm_s16le assets/work/voice_raw.wav

echo "footage: $(ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate,nb_frames -of csv=p=0 "$OUT")"
echo "voice:   $(ffprobe -v error -show_entries format=duration -of csv=p=0 assets/work/voice_raw.wav) s"
