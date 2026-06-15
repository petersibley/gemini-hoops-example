This is a simple script to show how to use the Google Gemini API or the
OpenAI API to generate 2D bounding boxes for objects in an image.

## Setup

```bash
export GEMINI_API_KEY=your-api-key-here
export OPENAI_API_KEY=your-api-key-here
```

You only need to set the API key for the provider you intend to use.

## Usage

```bash
uv run hoop_detect.py path/to/image.jpg -v -o annotated.png
uv run hoop_detect.py path/to/image.jpg -v -o annotated.png --provider openai
```

- `image_path`: local image to analyze
- `-o/--output`: where to save the annotated image (default: `<image>_annotated.png`)
- `-v/--verbose`: print detected objects and boxes to stdout
- `--provider`: `gemini` (default, uses `gemini-2.5-flash`) or `openai` (uses `gpt-4.1-mini`)

