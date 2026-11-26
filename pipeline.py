"""전체 파이프라인 (#10) — 모듈을 순서대로 연결하는 유일한 파일

실행: python pipeline.py "<YouTube URL>"
"""
import sys

from app.storage import save_result
from common.schema import LectureResult
from speech.align import align
from speech.stt import transcribe
from speech.summarize import summarize
from video.download import download
from video.slides import extract_slides


def process_lecture(url: str) -> LectureResult:
    meta = download(url)                          # A (#4)
    slides = extract_slides(meta.video_path)      # A (#5)
    segments = transcribe(meta.audio_path)        # B (#6)
    notes = align(slides, segments)               # B (#7)
    notes, overview = summarize(slides, notes)    # B (2단계)
    result = LectureResult(meta, slides, notes, overview)
    save_result(result)                           # C (#8)
    return result


if __name__ == "__main__":
    r = process_lecture(sys.argv[1])
    print(f"{r.meta.title}: slides={len(r.slides)} notes={len(r.notes)}")
