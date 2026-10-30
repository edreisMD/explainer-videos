# Evidence brief

Keep `brief.json` beside the video's editable sources. Beat timestamps are planning estimates until the audio or footage is timed. Revise them to match the export.

```json
{
  "title": "Why the queue matters",
  "audience": "An engineer reviewing a proposed architecture",
  "takeaway": "A queue decouples intake from worker availability.",
  "format": {"width": 1080, "height": 1920, "fps": 30},
  "sources": [{"id": "example", "locator": "Illustrative model; not a production benchmark"}],
  "beats": [
    {
      "id": "problem", "start": 0, "end": 6,
      "narration": "Tasks arrive even when the worker is busy.",
      "visual": "Three task tokens enter a waiting area beside one worker.",
      "claims": [{"text": "This is a conceptual example.", "source_ids": ["example"]}]
    },
    {
      "id": "mechanism", "start": 6, "end": 12,
      "narration": "A queue holds the next task until the worker is ready.",
      "visual": "The next token leaves the queue when the worker becomes free.",
      "claims": [{"text": "The example separates intake and execution.", "source_ids": ["example"]}]
    }
  ]
}
```

Use file paths and line numbers, commit/test reports, dataset identifiers, or primary-source URLs as locators. Source IDs make a claim traceable; their existence does not establish truth. Preserve units, denominators, measurement windows, and uncertainty for real numbers.

The validator allows different structures and durations. It checks positive dimensions/fps, finite ordered timestamps, unique IDs, narrative/visual plans, and resolvable claim references. It cannot judge factual accuracy, pacing, or visual execution.
