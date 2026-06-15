#!/usr/bin/env bash
set -euo pipefail

IMAGE_URL="https://en.wikipedia.org/wiki/Special:FilePath/Lifetime_Elite_Basketball_hoop.jpg"
IMAGE_FILE="hoop.jpg"

if [ ! -f "$IMAGE_FILE" ]; then
  curl -sL "$IMAGE_URL" -o "$IMAGE_FILE"
fi

uv run gemini_detect.py "$IMAGE_FILE" -v -o hoop_annotated.png

# To use OpenAI instead of Gemini:
#   uv run gemini_detect.py "$IMAGE_FILE" -v -o hoop_annotated.png --provider openai
