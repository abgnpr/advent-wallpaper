# Advent wallpaper

Make desktop wallpapers from original ASCII art with the cozy terminal colors of Advent of Code. An agent develops a scene from your idea; a local Python renderer turns the editable text into a full-resolution PNG. Rendering does not require an API key or an image-generation service.

## Create a wallpaper with an agent

Open this folder in your coding agent and ask, for example:

> Create an Advent of Code ASCII wallpaper of a tiny observatory on a snowy mountain, 2560x1440, with empty space on the left for icons.

The project's [AGENTS.md](AGENTS.md) points the agent to the [wallpaper skill](skills/aoc-wallpaper/SKILL.md). It will write the scene and render it using `uv`. This is a project-local skill referenced by AGENTS.md; it does not need to be installed globally. Automatic discovery and invocation may vary between agents.

## Render a scene yourself

Install [uv](https://docs.astral.sh/uv/) and run:

```sh
uv run advent-wallpaper examples/winter-forest.txt -o wallpapers/winter-forest.png
```

The first run installs the project's Python dependencies. The default output is 3840x2160. For example:

```sh
uv run advent-wallpaper examples/winter-forest.txt -o wallpapers/forest.png --size 1920x1080 --palette ice --position right
uv run advent-wallpaper --help
```

The renderer finds a system monospace font, or you can pass `--font /path/to/font.ttf`. Input is plain UTF-8 text containing printable ASCII, spaces and newlines; leading spaces are significant and tabs are rejected. Edit the text and rerun to refine a wallpaper. The renderer centers the scene vertically and fits it within the canvas, with an adjustable margin. It colors characters by category, so the same character always has the same color. Output files are PNGs; set one as your wallpaper using your desktop's usual settings.
