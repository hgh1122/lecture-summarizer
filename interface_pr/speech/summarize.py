"""[B] 요약 모듈 (2단계)"""
from common.schema import Note, Slide


def summarize(slides: list[Slide], notes: list[Note]) -> tuple[list[Note], str]:
    """슬라이드별 요약(map) + 강의 전체 요약(reduce)

    입력:  slides, notes(summary 비어 있음)
    출력:  (summary가 채워진 notes, overview 문자열)
    힌트:  Ollama 로컬 LLM
    1단계에서는 요약 없이 그대로 통과시킨다.
    """
    return notes, ""
