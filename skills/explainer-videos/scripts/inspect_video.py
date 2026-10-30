#!/usr/bin/env python3
"""Inspect exported video metadata with ffprobe. Does not judge content quality."""

import argparse
import json
import math
from pathlib import Path
import shutil
import subprocess


def inspect(path, width=None, height=None, audio="optional"):
    if not shutil.which("ffprobe"):
        raise ValueError("ffprobe is required; install FFmpeg before inspecting video")
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path.resolve())],
        capture_output=True, text=True, timeout=30,
    )
    if result.returncode:
        raise ValueError(result.stderr.strip() or "ffprobe could not read this file")
    metadata = json.loads(result.stdout)
    streams = metadata.get("streams", [])
    videos = [s for s in streams if s.get("codec_type") == "video" and not s.get("disposition", {}).get("attached_pic")]
    audios = [s for s in streams if s.get("codec_type") == "audio"]
    errors = []
    if not videos:
        errors.append("No video stream")
    video = videos[0] if videos else {}
    for label, expected in (("width", width), ("height", height)):
        if expected is not None and video.get(label) != expected:
            errors.append(f"Expected {label}={expected}, got {video.get(label)}")
    if audio == "required" and not audios:
        errors.append("Required audio stream is absent")
    raw_duration = metadata.get("format", {}).get("duration", video.get("duration"))
    try:
        duration = float(raw_duration)
    except (TypeError, ValueError):
        duration = 0
    if not math.isfinite(duration) or duration <= 0:
        errors.append("Missing or invalid positive duration")
    return {
        "status": "fail" if errors else "pass", "errors": errors,
        "width": video.get("width"), "height": video.get("height"),
        "fps": video.get("avg_frame_rate"), "duration_seconds": duration,
        "has_audio": bool(audios),
        "scope": "Metadata only; inspect playback, visuals, audio, and claims separately.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", type=Path)
    parser.add_argument("--width", type=int)
    parser.add_argument("--height", type=int)
    parser.add_argument("--audio", choices=("required", "optional"), default="optional")
    args = parser.parse_args()
    try:
        report = inspect(args.video, args.width, args.height, args.audio)
    except (ValueError, OSError, subprocess.TimeoutExpired) as exc:
        report = {"status": "fail", "errors": [str(exc)]}
    print(json.dumps(report, indent=2, allow_nan=False))
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
