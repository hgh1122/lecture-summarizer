"""[C] 결과 저장 모듈 (#8)"""
from common.schema import LectureResult


def save_result(result: LectureResult) -> None:
    """처리 결과 저장 (lectures / slides / notes)

    입력:  LectureResult
    샘플:  docs/samples/contract/result.json
    """
    raise NotImplementedError("#8")


def load_result(video_id: str) -> LectureResult:
    """저장된 결과 조회 -> LectureResult"""
    raise NotImplementedError("#8")
