#!/usr/bin/env bash
# Combine the silent Remotion render with the finished audio mix → the final MP4 (H.264 + AAC).
#   bash scripts/mux.sh [video] [audio] [output]
set -euo pipefail
VIDEO="${1:-out/video-silent.mp4}"
AUDIO="${2:-out/audio-mix.wav}"
OUT="${3:-out/WWCC-promo-1080x1920.mp4}"

# (no -shortest: the picture and the mix have the same length; -shortest would clip the last video frame)
ffmpeg -y -hide_banner -loglevel error -i "$VIDEO" -i "$AUDIO" \
  -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 256k -ar 48000 -ac 2 \
  -metadata title="Wagga Wagga Community Care – We're now open" \
  -movflags +faststart "$OUT"

echo "wrote $OUT"
ffprobe -v error -show_entries stream=codec_name,profile,width,height,r_frame_rate,pix_fmt,sample_rate,channels,duration -of default=nw=1 "$OUT"
