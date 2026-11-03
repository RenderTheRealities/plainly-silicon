#!/usr/bin/env bash
# One-time setup for a fresh workspace. Free tools only.
set -euo pipefail
cd "$(dirname "$0")"
pip install -q --break-system-packages --root-user-action=ignore kokoro-onnx soundfile numpy pillow
mkdir -p tts
B=https://huggingface.co/onnx-community/Kokoro-82M-v1.0-ONNX/resolve/main
[ -s tts/model.onnx ] || curl -sSL --max-time 600 -o tts/model.onnx "$B/onnx/model.onnx"
if [ ! -s tts/voices.npz ]; then
  curl -sSL --max-time 60 -o tts/am_michael.bin "$B/voices/am_michael.bin"
  python3 -c "import numpy as np; np.savez('tts/voices.npz', am_michael=np.fromfile('tts/am_michael.bin', dtype=np.float32).reshape(-1,1,256))"
fi
command -v ffmpeg >/dev/null || { echo "ffmpeg missing"; exit 1; }
echo "setup ok"
