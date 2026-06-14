# Plan: Gemini bounding-box + segmentation mask demo script

## Context

The repo is currently empty of code (just README + docs describing intent: "a simple script to show how to use the Google Gemini REST API to generate quick image labels"). The user wants a small, friend-shareable Python script demonstrating Gemini 2.5 Flash's "spatial understanding" capability — given a local image, ask Gemini for 2D bounding boxes AND segmentation masks for detected objects, then visualize/save the result locally. Keep it dead simple — no abstractions, one file.

## Research summary (from subagent + live testing)

- **SDK**: `google-genai` (new unified SDK), `pip install google-genai`. Import via `from google import genai` and `from google.genai import types`.
- **Auth**: `client = genai.Client()` picks up `GEMINI_API_KEY` / `GOOGLE_API_KEY` env var automatically. We'll rely on env var (no key handling code needed).
- **Model**: `gemini-3.5-flash` (the official cookbook's default `MODEL_ID` for the segmentation notebook). Note: `gemini-2.5-flash` is reachable on this account but returns an undocumented `<seg_NNN>` token format for `mask` instead of base64 PNG, so it's not usable for the mask path. `gemini-3.5-flash` returned a transient 503 (server overload) during testing — that's expected to clear; it's still the right model per the cookbook.
- **Prompt** (single call gets both bbox + mask, verbatim pattern from cookbook):
  > "Give the segmentation masks for the [objects/all prominent items in the image]. Output a JSON list of segmentation masks where each entry contains the 2D bounding box in the key \"box_2d\", the segmentation mask in key \"mask\", and the text label in the key \"label\". Use descriptive labels."
- **Config** (verbatim from cookbook — no `response_mime_type`, no `max_output_tokens`):
  ```python
  config = types.GenerateContentConfig(
      temperature=0.5,
      safety_settings=[types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_ONLY_HIGH")],
      thinking_config=types.ThinkingConfig(thinking_budget=0),
  )
  ```
  Image should be resized via `im.thumbnail([1024,1024], Image.Resampling.LANCZOS)` before sending, as in the cookbook.
- **Response format**: JSON list of `{"box_2d": [ymin, xmin, ymax, xmax], "label": str, "mask": "data:image/png;base64,..."}`. Coordinates normalized 0–1000, y-before-x. Mask PNG is sized to the bbox crop (not full image) and is a grayscale 0–255 probability map — needs resizing to bbox pixel dims and pasting into a full-size canvas, threshold ~127 for binary.
- **Robustness**: strip markdown code fences (` ```json `) from `response.text` before `json.loads`, per cookbook's `parse_json`. If a detection's `mask` field doesn't start with `data:image/png;base64,`, skip the mask overlay for that detection (but still draw its bbox+label) — don't special-case unknown token formats.

## Implementation

Single file: `gemini_detect.py` at repo root.

### Dependencies
- `google-genai`
- `Pillow` (image loading, drawing, mask compositing)
- `numpy` (mask array manipulation)

Add a `pyproject.toml` (uv-compatible, per `docs/uv.md`) declaring these deps, OR keep it minimal with just a comment header showing `pip install google-genai pillow numpy`. Given user wants "super simple" + uv is the documented tool, create a minimal `pyproject.toml` so `uv run gemini_detect.py` just works.

### Script structure (`gemini_detect.py`)

1. **CLI args** (argparse):
   - `image_path` (positional, required) — local input image
   - `-o/--output` (default: `<input_stem>_annotated.png`) — where to save annotated image
   - `-v/--verbose` — print progress / raw JSON to stdout

2. **Main flow**:
   - Load image with PIL, get width/height.
   - Build `genai.Client()`.
   - Send image + prompt asking for bbox + segmentation mask JSON for "prominent items" (generic, not hardcoded to one object class — good for demo flexibility).
   - Parse `response.text` as JSON (strip markdown fences defensively if present).
   - If verbose, print the parsed detections (labels + boxes) to stdout.

3. **Visualization**:
   - For each detection:
     - Convert `box_2d` (0-1000) → pixel coords using width/height.
     - Decode `mask` base64 PNG → grayscale, resize to bbox pixel size, threshold to binary.
     - Composite mask onto a full-size overlay (semi-transparent color fill) at the bbox location.
     - Draw bbox rectangle + label text on the image (PIL `ImageDraw`).
   - Use a small set of distinct colors cycling per detection for visual clarity.
   - Save the annotated image to the output path.

4. **Error handling**: minimal — guard clauses for missing API key (clear message pointing to `GEMINI_API_KEY` env var) and missing input file. No over-engineering.

### Supporting files

- `pyproject.toml`: minimal `[project]` with name, version, requires-python, dependencies (`google-genai`, `pillow`, `numpy`).
- `.gitignore`: add `.venv/`, `__pycache__/`, `*.pyc`, `.env`, and output images pattern (e.g. `*_annotated.png`) so demo outputs don't clutter git status.
- Update `README.md`: brief usage instructions — `export GEMINI_API_KEY=...`, `uv run gemini_detect.py path/to/image.jpg -v -o out.png`.

## Verification

1. `uv sync` / `uv run gemini_detect.py --help` — confirm CLI parses.
2. Run against a real local test image (user will need to supply one, or we can grab a small sample image) with `GEMINI_API_KEY` set, with `-v`, and confirm:
   - JSON detections print to stdout.
   - Output annotated PNG is written with bounding boxes + colored mask overlays + labels.
3. Sanity-check mask alignment visually (mask overlay should sit inside/around the drawn bbox, not offset).
