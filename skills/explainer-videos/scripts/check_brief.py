#!/usr/bin/env python3
"""Validate an explainer brief's structure, not its factual or visual quality."""

import argparse
import json
import math
from pathlib import Path


def number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def validate(brief):
    errors = []
    if not isinstance(brief, dict):
        return ["brief must be an object"]
    for key in ("title", "audience", "takeaway"):
        if not nonempty(brief.get(key)):
            errors.append(f"{key} must be nonempty text")
    fmt = brief.get("format")
    if not isinstance(fmt, dict):
        errors.append("format must be an object")
    else:
        for key in ("width", "height"):
            value = fmt.get(key)
            if type(value) is not int or value <= 0:
                errors.append(f"format.{key} must be a positive integer")
        if not number(fmt.get("fps")) or fmt["fps"] <= 0:
            errors.append("format.fps must be positive and finite")

    sources = brief.get("sources")
    source_ids = set()
    if not isinstance(sources, list):
        errors.append("sources must be a list")
    else:
        for index, source in enumerate(sources):
            if not isinstance(source, dict):
                errors.append(f"sources[{index}] must be an object")
                continue
            sid = source.get("id")
            if not nonempty(sid):
                errors.append(f"sources[{index}].id must be nonempty text")
            elif sid in source_ids:
                errors.append(f"duplicate source id: {sid}")
            else:
                source_ids.add(sid)
            if not nonempty(source.get("locator")):
                errors.append(f"sources[{index}].locator must identify evidence")

    beats = brief.get("beats")
    if not isinstance(beats, list) or not beats:
        return errors + ["beats must be a nonempty list"]
    beat_ids = set()
    previous_end = 0
    for index, beat in enumerate(beats):
        prefix = f"beats[{index}]"
        if not isinstance(beat, dict):
            errors.append(f"{prefix} must be an object")
            continue
        bid = beat.get("id")
        if not nonempty(bid):
            errors.append(f"{prefix}.id must be nonempty text")
        elif bid in beat_ids:
            errors.append(f"duplicate beat id: {bid}")
        else:
            beat_ids.add(bid)
        start, end = beat.get("start"), beat.get("end")
        if not number(start) or not number(end):
            errors.append(f"{prefix} timestamps must be finite numbers")
        elif start < 0 or end <= start or start < previous_end:
            errors.append(f"{prefix} must have positive duration and not overlap the previous beat")
        else:
            previous_end = end
        for key in ("narration", "visual"):
            if not nonempty(beat.get(key)):
                errors.append(f"{prefix}.{key} must be nonempty text")
        claims = beat.get("claims")
        if not isinstance(claims, list):
            errors.append(f"{prefix}.claims must be a list (empty for a claim-free beat)")
            continue
        for ci, claim in enumerate(claims):
            location = f"{prefix}.claims[{ci}]"
            if not isinstance(claim, dict) or not nonempty(claim.get("text")):
                errors.append(f"{location} must include claim text")
                continue
            refs = claim.get("source_ids")
            if not isinstance(refs, list) or not refs:
                errors.append(f"{location} needs source_ids")
                continue
            for sid in refs:
                if not isinstance(sid, str) or sid not in source_ids:
                    errors.append(f"{location} references unknown source: {sid!r}")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("brief", type=Path)
    args = parser.parse_args()
    try:
        errors = validate(json.loads(args.brief.read_text()))
    except (OSError, ValueError) as exc:
        errors = [str(exc)]
    print(json.dumps({"status": "fail" if errors else "pass", "errors": errors,
                      "scope": "Structure and source references only; facts require review."}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
