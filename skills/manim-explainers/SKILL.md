---
name: manim-explainers
description: Create animated explainer videos with Manim Community for concepts, algorithms, architecture, and agent work. Use when the user requests Manim or diagram-led animation, including dark or light themes; use real screen capture for claims about actual UI behavior.
---

# Manim explainers

Use animated geometry to build an explanation. Favor an original visual identity: consistent semantic colors, sparse labels, deliberate motion, and concrete examples.

## Story and evidence

Identify the viewer's question, one takeaway, and evidence for material claims. Read source artifacts. Label invented examples as illustrative. Distinguish proposed and completed work. For an agent update, show the starting state, the change, and its practical consequence. For a concept, introduce an example, reveal the mechanism, then generalize.

Write narration and a scene plan first. Use an available authorized voice or supplied audio; do not clone or imitate a named person's voice. Time scenes to actual audio and retain captions or a transcript. For silent videos, provide readable on-screen explanation and identify them as silent.

## Build from the starter

Copy `assets/scene.py` into the video's output directory and replace its illustrative queue example with the requested explanation. It is runnable, not a universal diagram generator. Read [rendering](references/rendering.md) for installation, commands, aspect ratios, voice integration, and output validation.

The starter supports `EXPLAINER_THEME=dark` and `light`, with `EXPLAINER_FORMAT=vertical` or `landscape`. Choose the user's preference; default to dark for diagrams and vertical for a phone feed. These are editable presets. Both map blue to input/context, amber to work/change, and green to result. Adapt the semantics to the topic, then keep them consistent.

## Scene craft

- Show one causal step at a time. A moving token, queue, highlighted edge, or transformed object should explain something specific.
- Reuse objects across beats so viewers track identity. Use `Transform` when the same thing changes; replace or fade when it is different.
- Keep text short and check bounding boxes. Wrap labels deliberately before scaling; tiny text is not a fit strategy. Use `Text` for prose so LaTeX is unnecessary; use `MathTex` when mathematical typesetting is needed and available.
- Use measured pauses around important changes. Continuous motion and forced loops are optional.
- Fit the actual frame geometry. Reserve quiet top/bottom margins for player UI and captions. Inspect the smallest intended playback size.

## Finish

Render a preview first. Inspect the beginning, every transition, the key causal moment, and ending; listen to narration if present. Repair clipping, illegible labels, mismatched timing, unsupported claims, and misleading scale. After three unsuccessful render/repair cycles, return the blocker and usable artifacts.

Deliver the final video, source, transcript/captions if present, and what was checked. Uploading or posting requires authorization. This skill works on its own; `$explainer-videos` can supply a richer evidence brief when installed.
