#!/usr/bin/env bash
# One-time setup for a fresh workspace. Free tools only.
set -euo pipefail
cd "$(dirname "$0")"
# python3 may be a different version than pip's default; install for the interpreter the scripts use
python3 -m pip install -q --break-system-packages --root-user-action=ignore kokoro-onnx soundfile numpy
python3 -c "import PIL.Image" 2>/dev/null || python3 -m pip install -q --break-system-packages --root-user-action=ignore --ignore-installed pillow
mkdir -p tts
B=https://huggingface.co/onnx-community/Kokoro-82M-v1.0-ONNX/resolve/main
# fallback when huggingface.co is blocked: the same Kokoro v1.0 model from the kokoro-onnx GitHub release
GB=https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0
if [ ! -s tts/model.onnx ]; then
  curl -sSfL --max-time 600 -o tts/model.onnx "$B/onnx/model.onnx" || curl -sSfL --max-time 900 -o tts/model.onnx "$GB/kokoro-v1.0.onnx"
fi
if [ ! -s tts/voices.npz ]; then
  if curl -sSfL --max-time 60 -o tts/am_michael.bin "$B/voices/am_michael.bin"; then
    python3 -c "import numpy as np; np.savez('tts/voices.npz', am_michael=np.fromfile('tts/am_michael.bin', dtype=np.float32).reshape(-1,1,256))"
  else
    curl -sSfL --max-time 300 -o tts/voices-v1.0.bin "$GB/voices-v1.0.bin"
    python3 -c "import numpy as np; v=np.load('tts/voices-v1.0.bin'); np.savez('tts/voices.npz', am_michael=v['am_michael'].reshape(-1,1,256).astype(np.float32))"
  fi
fi
# Poppins and Lora (used by several themes) are not always installed
GF=/usr/share/fonts/truetype/google-fonts
if [ ! -s $GF/Lora-Variable.ttf ]; then
  mkdir -p $GF
  R=https://raw.githubusercontent.com/google/fonts/main/ofl
  for f in Poppins-Bold Poppins-Medium Poppins-Regular; do curl -sSfL --max-time 60 -o $GF/$f.ttf $R/poppins/$f.ttf; done
  curl -sSfL --max-time 60 -o $GF/Lora-Variable.ttf "$R/lora/Lora%5Bwght%5D.ttf"
fi
command -v ffmpeg >/dev/null || { echo "ffmpeg missing"; exit 1; }
echo "setup ok"
