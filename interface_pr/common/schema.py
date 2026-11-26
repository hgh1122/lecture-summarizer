"""모듈 간 데이터 계약 (Module contract)

- 모든 모듈은 이 파일의 데이터 클래스로만 입력/출력을 주고받는다.
- 시간 값은 모두 초(float) 단위.
- 이 파일을 수정하면 모든 모듈의 약속이 바뀌므로, 별도 PR + 팀원 전원 리뷰 후 머지한다.
"""
from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, field


@dataclass
class VideoMeta:
    """download() 의 출력"""
    video_id: str
    title: str
    video_path: str          # 예: "data/abc123/video.mp4"
    audio_path: str          # 16kHz mono wav
    duration: float          # 초


@dataclass
class Slide:
    """extract_slides() 의 출력 원소"""
    no: int                  # 1부터 시작
    start: float             # 슬라이드가 나타난 시각 (초)
    end: float               # 슬라이드가 사라진 시각 (초)
    image_path: str          # 캡처 이미지 경로
    ocr_text: str            # 인식된 글자, 줄바꿈은 "\n"


@dataclass
class Segment:
    """transcribe() 의 출력 원소"""
    start: float
    end: float
    text: str


@dataclass
class Note:
    """align() / summarize() 의 출력 원소"""
    slide_no: int            # Slide.no 와 짝
    transcript: str          # 해당 슬라이드 구간의 발화 전체
    summary: str = ""        # 2단계 전에는 빈 문자열
    keywords: list[str] = field(default_factory=list)


@dataclass
class LectureResult:
    """파이프라인 최종 결과 (서비스 계층 입력)"""
    meta: VideoMeta
    slides: list[Slide]
    notes: list[Note]
    overview: str = ""       # 강의 전체 요약


# ---------------------------------------------------------------- JSON 입출력
def save_json(obj, path: str) -> str:
    """데이터 클래스(또는 그 리스트)를 JSON 파일로 저장"""
    if isinstance(obj, list):
        data = [asdict(x) for x in obj]
    else:
        data = asdict(obj)
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return path


def _read(path: str):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_meta(path: str) -> VideoMeta:
    return VideoMeta(**_read(path))


def load_slides(path: str) -> list[Slide]:
    return [Slide(**d) for d in _read(path)]


def load_segments(path: str) -> list[Segment]:
    return [Segment(**d) for d in _read(path)]


def load_notes(path: str) -> list[Note]:
    return [Note(**d) for d in _read(path)]


def load_result(path: str) -> LectureResult:
    d = _read(path)
    return LectureResult(
        meta=VideoMeta(**d["meta"]),
        slides=[Slide(**s) for s in d["slides"]],
        notes=[Note(**n) for n in d["notes"]],
        overview=d.get("overview", ""),
    )


if __name__ == "__main__":
    # 샘플 데이터가 계약과 맞는지 확인: python -m common.schema
    base = "docs/samples/contract"
    print(load_meta(f"{base}/video_meta.json"))
    print(len(load_slides(f"{base}/slides.json")), "slides")
    print(len(load_segments(f"{base}/segments.json")), "segments")
    print(len(load_notes(f"{base}/notes.json")), "notes")
    r = load_result(f"{base}/result.json")
    print("result OK:", r.meta.title, len(r.slides), len(r.notes))
