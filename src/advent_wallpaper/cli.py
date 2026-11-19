"""Render a plain-text ASCII scene on a desktop-sized canvas."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageColor, ImageDraw, ImageFilter, ImageFont

PALETTES = {
    "advent": {"background": "#0f0f23", "text": "#cccccc", "green": "#00cc66", "bright": "#99ff99", "star": "#ffff66", "snow": "#c4e4ff"},
    "amber": {"background": "#17120c", "text": "#e7c99a", "green": "#e99a36", "bright": "#ffe0a0", "star": "#fff0bc", "snow": "#f6d8a5"},
    "ice": {"background": "#0b1725", "text": "#bad2df", "green": "#4bc0c8", "bright": "#b8fff5", "star": "#fff4b0", "snow": "#e6f8ff"},
}


def dimensions(value: str) -> tuple[int, int]:
    try:
        width, height = (int(part) for part in value.lower().split("x"))
        if not (1 <= width <= 16384 and 1 <= height <= 16384):
            raise ValueError
        return width, height
    except ValueError as exc:
        raise argparse.ArgumentTypeError("size must be WIDTHxHEIGHT, each between 1 and 16384") from exc


def find_font() -> str:
    if shutil.which("fc-match"):
        result = subprocess.run(["fc-match", "-f", "%{file}", "monospace"], capture_output=True, text=True, check=False)
        if result.returncode == 0 and Path(result.stdout).is_file():
            return result.stdout
    for path in ("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", "/System/Library/Fonts/Menlo.ttc", "C:/Windows/Fonts/consola.ttf"):
        if Path(path).is_file():
            return path
    raise ValueError("No monospace font found; supply a font with --font PATH")


def render(scene: str, size: tuple[int, int], font_path: str, palette: dict[str, str], margin: float, position: str, glow: bool) -> Image.Image:
    scene = scene.replace("\r\n", "\n").replace("\r", "\n").strip("\n")
    if not scene.strip():
        raise ValueError("the scene is empty")
    if any(ord(c) < 32 and c != "\n" or ord(c) > 126 for c in scene):
        raise ValueError("scene must contain printable ASCII and newlines only; replace tabs with spaces")
    lines = scene.split("\n")
    columns = max(map(len, lines))
    width, height = size
    available_width, available_height = width * (1 - 2 * margin), height * (1 - 2 * margin)

    def metrics(points: int):
        font = ImageFont.truetype(font_path, points)
        cell = font.getlength("M")
        ascent, descent = font.getmetrics()
        line_height = ascent + descent
        return font, cell, line_height

    # Choose the largest size that fits both dimensions, retaining a fixed character grid.
    low, high = 1, max(width, height) + 1
    while low < high:
        mid = (low + high + 1) // 2
        _, cell, line_height = metrics(mid)
        if cell * columns <= available_width and line_height * len(lines) <= available_height:
            low = mid
        else:
            high = mid - 1
    font, cell, line_height = metrics(low)
    if cell * columns > available_width or line_height * len(lines) > available_height:
        raise ValueError("scene is too large to fit the requested canvas, even at 1px font size")
    block_width, block_height = cell * columns, line_height * len(lines)
    x = {"left": width * margin, "center": (width - block_width) / 2, "right": width * (1 - margin) - block_width}[position]
    y = (height - block_height) / 2
    layer = Image.new("RGBA", size)
    draw = ImageDraw.Draw(layer)
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == " ":
                continue
            color = palette["star"] if char in "*+" else palette["snow"] if char in ".,:" else palette["bright"] if char in "@oO" else palette["green"] if char in "/\\|^_#~" else palette["text"]
            draw.text((round(x + col * cell), round(y + row * line_height)), char, font=font, fill=ImageColor.getrgb(color) + (255,))
    image = Image.new("RGBA", size, ImageColor.getrgb(palette["background"]) + (255,))
    if glow:
        blurred = layer.filter(ImageFilter.GaussianBlur(max(1, low / 8)))
        blurred.putalpha(blurred.getchannel("A").point(lambda alpha: alpha * 3 // 4))
        image.alpha_composite(blurred)
    image.alpha_composite(layer)
    return image.convert("RGB")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scene", type=Path, help="UTF-8 text file containing printable ASCII art")
    parser.add_argument("-o", "--output", type=Path, required=True, help="output PNG path")
    parser.add_argument("--size", type=dimensions, default=(3840, 2160), metavar="WIDTHxHEIGHT", help="canvas size (default: 3840x2160)")
    parser.add_argument("--font", help="path to a monospace font (default: system monospace)")
    parser.add_argument("--palette", choices=PALETTES, default="advent")
    parser.add_argument("--margin", type=float, default=0.1, help="minimum margin as a fraction of each dimension (default: 0.1)")
    parser.add_argument("--position", choices=("left", "center", "right"), default="center", help="horizontal alignment")
    parser.add_argument("--no-glow", action="store_true", help="disable the subtle terminal glow")
    args = parser.parse_args()
    if not 0 <= args.margin < 0.5:
        parser.error("--margin must be at least 0 and less than 0.5")
    if args.output.suffix.lower() != ".png":
        parser.error("output must have a .png extension")
    try:
        image = render(args.scene.read_text(encoding="utf-8"), args.size, args.font or find_font(), PALETTES[args.palette], args.margin, args.position, not args.no_glow)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        image.save(args.output, format="PNG")
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
    print(f"Wrote {args.output} ({image.width}x{image.height})")


if __name__ == "__main__":
    main()
