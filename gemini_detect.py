#!/usr/bin/env python3
"""Detect objects and draw bounding boxes in an image using Gemini 2.5 Flash."""

import argparse
import json
import sys
from pathlib import Path

from google import genai
from google.genai import types
from PIL import Image, ImageDraw

MODEL = "gemini-2.5-flash"

PROMPT = (
    "Detect the basketball hoop, meaning the rim and net together as a "
    "single object. Output a JSON list with one entry whose bounding box "
    "tightly encloses just the rim and net, excluding the backboard. The "
    'entry should contain the 2D bounding box in the key "box_2d" as '
    "[ymin, xmin, ymax, xmax] normalized to 0-1000, and a descriptive label "
    'in the key "label".'
)

COLORS = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 128, 255),
    (255, 255, 0),
    (255, 0, 255),
    (0, 255, 255),
    (255, 128, 0),
    (128, 0, 255),
]


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image_path", type=Path, help="path to a local image")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="path to save the annotated image (default: <image>_annotated.png)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="print progress and raw detections to stdout",
    )
    return parser.parse_args()


def strip_code_fence(text):
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1]
        text = text.rsplit("```", 1)[0]
    return text.strip()


def box_to_pixels(box_2d, width, height):
    ymin, xmin, ymax, xmax = box_2d
    return (
        int(xmin / 1000 * width),
        int(ymin / 1000 * height),
        int(xmax / 1000 * width),
        int(ymax / 1000 * height),
    )


def annotate(image, detections, verbose):
    width, height = image.size
    draw = ImageDraw.Draw(image)

    for i, detection in enumerate(detections):
        color = COLORS[i % len(COLORS)]
        label = detection.get("label", "")
        box_px = box_to_pixels(detection["box_2d"], width, height)
        x0, y0, _, _ = box_px

        if verbose:
            print(f"  {label}: box={box_px}")

        draw.rectangle(box_px, outline=color, width=3)
        draw.text((x0 + 4, y0 + 4), label, fill=color)

    return image


def main():
    args = parse_args()

    if not args.image_path.exists():
        sys.exit(f"Image not found: {args.image_path}")

    output_path = args.output or args.image_path.with_name(
        f"{args.image_path.stem}_annotated.png"
    )

    image = Image.open(args.image_path)
    image.thumbnail((1024, 1024), Image.Resampling.LANCZOS)

    if args.verbose:
        print(f"Loaded {args.image_path} ({image.width}x{image.height})")
        print("Calling Gemini...")

    client = genai.Client()
    response = client.models.generate_content(
        model=MODEL,
        contents=[PROMPT, image],
        config=types.GenerateContentConfig(
            temperature=0.5,
            thinking_config=types.ThinkingConfig(thinking_budget=0),
        ),
    )

    detections = json.loads(strip_code_fence(response.text))

    if args.verbose:
        print(f"Found {len(detections)} object(s):")

    annotated = annotate(image, detections, args.verbose)
    annotated.save(output_path)

    print(f"Saved annotated image to {output_path}")


if __name__ == "__main__":
    main()
