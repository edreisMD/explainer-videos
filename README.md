# explainer-videos

Skills that help agents explain their work through videos people can understand.

Inspired by [Andrej Karpathy's post about richer ways to understand model outputs](https://x.com/karpathy/status/2105819303471976479). An independent project by [Eduardo Reis](https://edreis.ai); no endorsement or particular rendering/voice service is implied.

The aim: read the evidence, find one takeaway, show the mechanism, synchronize the story, and inspect the export.

## Skills

| Skill | Use it for |
| --- | --- |
| [explainer-videos](skills/explainer-videos/SKILL.md) | Evidence, storyboarding, style selection, narration, quality review, and delivery. Includes brief validation and video inspection helpers. |
| [manim-explainers](skills/manim-explainers/SKILL.md) | Animated diagrams and technical concepts. Original dark/light themes, vertical/landscape formats, and a runnable Manim starter. |
| [screen-demo-explainers](skills/screen-demo-explainers/SKILL.md) | Real software walkthroughs, feature demonstrations, and before/after explanations. |

Each folder follows the [Agent Skills format](https://agentskills.io/specification) and installs separately. The general workflow can route to specialist skills when installed. These instructions/tools work independently of [AgentFeed](https://agentfeed.com); no hosted service, screen recorder, or narration subscription is included.

## Install

Clone and copy the desired folders into your agent's skills directory. For Codex:

```sh
git clone https://github.com/edreisMD/explainer-videos.git
mkdir -p ~/.codex/skills
cp -R explainer-videos/skills/explainer-videos ~/.codex/skills/
cp -R explainer-videos/skills/manim-explainers ~/.codex/skills/
cp -R explainer-videos/skills/screen-demo-explainers ~/.codex/skills/
```

Inspect an existing destination before copying. Other agents use their own skill locations. Installing a skill does not install its renderer.

## Use

> Use $explainer-videos to explain this PR to a product manager in a one-minute video. Use the diff and test results as evidence. Show what changed and why it matters.

> Use $manim-explainers to explain how a queue separates intake from execution. Use the light theme, a vertical frame, and a concrete example.

> Use $screen-demo-explainers to show the new onboarding flow using demo data and captions.

For the Manim starter, install [uv](https://docs.astral.sh/uv/) and the system dependencies in [Manim's installation guide](https://docs.manim.community/en/stable/installation/uv.html), then:

```sh
uv sync --extra render
EXPLAINER_PREVIEW=1 uv run --extra render manim render \
  --media_dir output/preview skills/manim-explainers/assets/scene.py ExplainerScene
```

The starter is a silent illustrative example, not a completed explanation of arbitrary work. See [rendering](skills/manim-explainers/references/rendering.md) for full resolution, themes, and audio.

## Add a style

Add an independently useful `skills/<style-name>/SKILL.md` with a precise name/description. Explain when it helps, how agents produce it using available tools, and what to inspect. Include a runnable example when useful. Keep provider-specific dependencies optional and explicit.

Styles can change the visual grammar, pacing, and renderer while preserving grounded claims, readable output, honest verification, and the user's publishing permissions. Don't require another style's voice, aspect ratio, or toolchain. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Checks and license

`python3 -m unittest discover -s tests` tests brief validation and actual FFmpeg inspection when available. `uv sync --extra render` enables the starter. The starter has been preview-rendered in dark vertical and light landscape formats with Manim 0.19.0 / Python 3.12. These are silent examples; metadata and representative frames were checked, not narration quality. Full-resolution output and other systems are not covered by that smoke test.

MIT. Third-party renderers, fonts, media, and voice services retain their own terms. No private AgentFeed configuration, credentials, or voice assets are included.
