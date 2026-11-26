"""[A] 슬라이드 추출 모듈 (#5)"""
from common.schema import Slide


def extract_slides(video_path: str, out_dir: str | None = None) -> list[Slide]:
    """영상 -> 슬라이드 전환 구간 검출 + 키프레임 캡처 + OCR

    입력:  video_path  다운로드된 mp4 경로
    출력:  list[Slide] (no 1부터, start/end 초 단위, image_path, ocr_text)
    샘플:  docs/samples/contract/slides.json
    힌트:  PySceneDetect (전환 감지), OpenCV (캡처), EasyOCR (ko, en)
    """
    raise NotImplementedError("#5")
