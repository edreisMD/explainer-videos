# Rendering with Manim Community

The starter targets Manim Community 0.19.0 with Python 3.12. Do not mix it with the separate `manimlib` engine. In this repository, `uv sync --extra render` uses `.python-version` and installs the pinned renderer. Its older PyAV dependency is not compatible with every newer Python/FFmpeg combination, so keep this environment separate. Elsewhere use a project-local environment; Cairo/Pango system dependencies may be needed. Follow the [official installation guide](https://docs.manim.community/en/stable/installation/uv.html).

Copy `assets/scene.py` into the video's working directory. From this repository:

```sh
# Preview: 360 x 640, 15 fps. Silent and captioned.
EXPLAINER_PREVIEW=1 uv run --extra render manim render \
  --media_dir output/preview skills/manim-explainers/assets/scene.py ExplainerScene

# Final: 1080 x 1920, 30 fps. Light theme.
EXPLAINER_THEME=light uv run --extra render manim render \
  --media_dir output/final skills/manim-explainers/assets/scene.py ExplainerScene

# Landscape: 1920 x 1080 (640 x 360 in preview).
EXPLAINER_FORMAT=landscape uv run --extra render manim render \
  --media_dir output/landscape skills/manim-explainers/assets/scene.py ExplainerScene
```

Avoid quality presets that overwrite intended dimensions. The scene sets pixel resolution and frame geometry. Use distinct output directories for variants. See [configuration](https://docs.manim.community/en/stable/guides/configuration.html) and [text rendering](https://docs.manim.community/en/stable/guides/using_text.html).

`fit_text` checks width. Replace the starter's wording/graphics with the requested subject; the queue example is not measured performance. Change timing after recording narration. For supplied audio, `self.add_sound` places clips at current scene time; let the whole clip finish before advancing. For new narration, use an installed authorized tool, retain actual timings, and create captions from actual alignment. This library supplies no voice service or API key.

Use the exact video path printed by Manim, then inspect frames and playback. The general skill's optional `inspect_video.py` checks output metadata. Without it, use `ffprobe -v error -show_streams -show_format -of json /path/to/video.mp4`. Include source and transcript; do not report a narrated result when only the silent starter was rendered.
