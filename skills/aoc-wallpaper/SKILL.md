---
name: aoc-wallpaper
description: Create an Advent of Code inspired ASCII desktop wallpaper from a user's idea, using this project's text-to-PNG renderer.
---

# Create an ASCII wallpaper

Interpret the user's idea as an original, hand-composed text scene with the cozy terminal aesthetic of Advent of Code. Build a cohesive composition using printable ASCII characters and spaces only; no tabs, ANSI escapes, Unicode or markdown fences in the scene file. Preserve leading spaces, aligned rows, and intentional negative space. Use `*` or `+` for warm stars, `.`, `,`, `:` for cool details, `@`, `o`, `O` for bright accents, and `/`, `\`, `|`, `^`, `_`, `#`, `~` for green structural elements in the default palette. Other characters are neutral. The renderer applies these colors globally, not semantically.

1. Write the original scene to a descriptive `.txt` file under `wallpapers/`. Compose it for the requested subject and screen aspect ratio; leave room for desktop icons if requested. Avoid copying existing Advent of Code artwork.
2. Render it from the project root: `uv run advent-wallpaper wallpapers/NAME.txt -o wallpapers/NAME.png --size WIDTHxHEIGHT`. Default to 3840x2160 if no resolution is provided. See `uv run advent-wallpaper --help` for palettes, positioning, margins, fonts and glow.
3. Inspect the resulting image when possible; correct clipped or visually unclear art and rerender. Return links to both the PNG and editable text. Do not change the user's desktop background unless explicitly requested.

The LLM/agent writes the art; the renderer does not call a model. Users can refine the text and rerun the command without regenerating the scene.
