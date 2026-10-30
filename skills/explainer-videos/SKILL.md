---
name: explainer-videos
description: Turn agent work, research, or a technical concept into an explainer video with a grounded story, synchronized visuals, and checked delivery. Use when the user asks for a video explanation or video update; ordinary text answers do not trigger rendering.
---

# Explainer videos

Make the viewer understand one thing they can use. A video should show the mechanism, result, or decision that prose makes difficult to follow. Render the requested artifact; a script or storyboard alone is an intermediate result unless that is what the user asked for.

## Scope the explanation

Use the conversation and work artifacts to identify the audience, takeaway, evidence, and destination. Default a short agent update to 45–90 seconds, but adapt to the subject. Use 9:16 for a phone feed, 16:9 for a desktop explanation; honor explicit dimensions. Do not turn every answer into a video or assume the user wants uploads or paid narration.

Read the actual diff, test output, measurements, or paper before writing. Distinguish implemented, tested, proposed, and illustrative. Every material factual claim needs an identifiable source. Label toy examples on screen; never present an animation as a recorded run or a synthetic number as a benchmark.

## Choose the visual language

- **Manim diagrams:** mechanisms, architecture, algorithms, causal relationships. If available, use `$manim-explainers`; otherwise implement an equivalent scene with installed tools.
- **Screen demonstration:** visible product behavior or a workflow. If available, use `$screen-demo-explainers`.
- **Editorial cards:** a short update with a few facts. Use restrained typography and a diagram or concrete artifact; avoid a wall of text spread across slides.

Keep shared story decisions independent of the rendering engine. An explicit style request takes precedence over these defaults.

## Build the story before polishing

Write a brief using [the brief contract](references/brief.md). Open with the question or result, establish the starting state, show a change or mechanism, demonstrate the consequence, and close with the takeaway or decision. These are story functions, not a required number of scenes.

Prefer a concrete example over a feature list. Keep stable names and colors for the same entities. Each beat should explain why its visual exists. Animate relationships, state changes, data flow, or comparisons; avoid decorative motion and animated paragraphs.

Run `python scripts/check_brief.py /absolute/path/brief.json` from this skill directory. This checks structure and source references, not whether the evidence is true. Inspect the evidence yourself.

## Narration and timing

Choose an available local or authorized TTS engine, or accept supplied audio. Never imply that a provider, subscription, voice, or key exists. Use a neutral original voice rather than imitating a named person. Estimate 120–160 spoken words per minute, then time the actual recording.

Align visuals to recorded narration, not word-count estimates. Bring in an object when it is named and allow time to inspect it. Keep separate narration, scene timing, and captions so revisions can be regenerated. Do not invent word timestamps. Without alignment data, use sentence-level captions. Captioned silent delivery is valid if requested or if audio is unavailable; disclose it.

## Render, inspect, deliver

Render a low-resolution preview, inspect representative frames including transitions, and listen through narrated output. Check text at viewing size, overlap, contrast, safe margins, continuity, and whether motion teaches the intended idea. Then render the final format and run `python scripts/inspect_video.py final.mp4 --width 1080 --height 1920 --audio required` (use `optional` for silent output).

Read [the quality rubric](references/quality.md). Fix observed issues; do not claim checks that were not performed. A technical pass from ffprobe is not a story-quality pass. Stop after three failed render/repair cycles and report the remaining blocker with usable source or preview.

Deliver the video, transcript/captions when produced, source scene, evidence brief, and verification limits. Keep outputs local unless the user requested sharing. A rendered video is not permission to publish, message another user, or upload private work.
