import copy
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills/explainer-videos/scripts"


def load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


check = load("check_brief")
video = load("inspect_video")


class BriefValidation(unittest.TestCase):
    def setUp(self):
        self.brief = {
            "title": "Queues", "audience": "Engineers", "takeaway": "Separate intake and execution",
            "format": {"width": 1080, "height": 1920, "fps": 30},
            "sources": [{"id": "toy", "locator": "Illustrative model"}],
            "beats": [{"id": "one", "start": 0, "end": 4,
                       "narration": "A queue holds work.", "visual": "A token waits.",
                       "claims": [{"text": "This is an illustration", "source_ids": ["toy"]}]}],
        }

    def test_valid_brief(self):
        self.assertEqual(check.validate(self.brief), [])

    def test_unresolved_claim(self):
        self.brief["beats"][0]["claims"][0]["source_ids"] = ["missing"]
        self.assertTrue(any("unknown source" in e for e in check.validate(self.brief)))

    def test_overlapping_beats(self):
        beat = copy.deepcopy(self.brief["beats"][0])
        beat.update(id="two", start=3, end=8)
        self.brief["beats"].append(beat)
        self.assertTrue(any("overlap" in e for e in check.validate(self.brief)))

    def test_nonfinite_or_boolean_time(self):
        for value in (float("nan"), float("inf"), True):
            with self.subTest(value=value):
                self.brief["beats"][0]["end"] = value
                self.assertTrue(check.validate(self.brief))

    def test_malformed_source_reference(self):
        self.brief["beats"][0]["claims"][0]["source_ids"] = [{"id": "toy"}]
        self.assertTrue(check.validate(self.brief))

    def test_invalid_formats_and_root(self):
        self.assertTrue(check.validate([]))
        self.brief["format"]["width"] = True
        self.assertTrue(check.validate(self.brief))


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg/ffprobe not installed")
class ActualVideoInspection(unittest.TestCase):
    def test_silent_and_narrated_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            silent = Path(tmp) / "silent.mp4"
            subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "color=c=blue:s=90x160:r=15:d=1",
                            "-c:v", "libx264", "-pix_fmt", "yuv420p", str(silent)], check=True)
            self.assertEqual(video.inspect(silent, 90, 160)["status"], "pass")
            self.assertEqual(video.inspect(silent, 90, 160, "required")["status"], "fail")
            self.assertEqual(video.inspect(silent, 160, 90)["status"], "fail")
            narrated = Path(tmp) / "audio.mp4"
            subprocess.run(["ffmpeg", "-v", "error", "-i", str(silent), "-f", "lavfi", "-i",
                            "sine=frequency=440:duration=1", "-c:v", "copy", "-c:a", "aac", "-shortest", str(narrated)], check=True)
            report = video.inspect(narrated, 90, 160, "required")
            self.assertEqual(report["status"], "pass")
            self.assertTrue(report["has_audio"])
            broken = Path(tmp) / "broken.mp4"
            broken.write_text("not a video")
            with self.assertRaises(ValueError):
                video.inspect(broken)


if __name__ == "__main__":
    unittest.main()
