#!/usr/bin/env bash
set -euo pipefail
python -m pip install --user -r requirements.txt
mkdir -p outputs/downloads outputs/profile outputs/audio outputs/clips
python -m compileall -q scripts
ffmpeg -version | head -n 1
printf 'Setup complete. Read README.md; keep port 6080 PRIVATE.\n'
