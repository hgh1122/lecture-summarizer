"""[B] 슬라이드–음성 정렬 모듈 (#7)"""
from common.schema import Note, Segment, Slide


def align(slides: list[Slide], segments: list[Segment]) -> list[Note]:
    """발화 구간을 그 시각에 떠 있던 슬라이드에 배정

    입력:  slides    docs/samples/contract/slides.json
           segments  docs/samples/contract/segments.json
    출력:  list[Note] (슬라이드마다 1개, summary는 빈 문자열)
    샘플:  docs/samples/contract/notes.json  ← 위 두 샘플을 넣으면 이 결과가 나와야 함
    힌트:  구간 중심 시각 (start + end) / 2 가 [slide.start, slide.end) 안에 있으면 배정
    """
    raise NotImplementedError("#7")
