This is a simple script to show how to use the Google Gemini API to generate
2D bounding boxes for objects in an image.

## Setup

```bash
export GEMINI_API_KEY=your-api-key-here
```

## Usage

```bash
uv run gemini_detect.py path/to/image.jpg -v -o annotated.png
```

- `image_path`: local image to analyze
- `-o/--output`: where to save the annotated image (default: `<image>_annotated.png`)
- `-v/--verbose`: print detected objects and boxes to stdout

