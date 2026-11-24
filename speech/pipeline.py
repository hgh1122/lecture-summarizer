"""[B] 전체 흐름: slides.json -> notes.json  (B → C 인터페이스: docs/interface.md)"""
import os

from common import load_json, save_json
from speech.align import align
from speech.stt import transcribe
from speech.summarize import summarize_all


def run(slides_json_path, use_summary=True):
    a = load_json(slides_json_path)
    segments = transcribe(a["audio_path"])
    notes = align(a["slides"], segments)
    if use_summary:
        notes = summarize_all(notes)
    data = {"video_id": a["video_id"], "title": a["title"], "duration": a["duration"],
            "segments": segments, "notes": notes}
    out = os.path.join(os.path.dirname(slides_json_path), "notes.json")
    save_json(data, out)
    return out
