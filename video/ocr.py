"""[A] 1단계: 슬라이드 글자 인식 (EasyOCR)"""
import easyocr

_reader = None


def get_reader():
    global _reader
    if _reader is None:  # 모델 로딩이 느려서 한 번만 만듦
        _reader = easyocr.Reader(["ko", "en"])  # GPU 있으면 자동 사용
    return _reader


def read_text(image_path):
    """이미지 -> 위에서 아래 순서의 글자 (줄바꿈으로 연결)."""
    lines = get_reader().readtext(image_path, detail=0, paragraph=True)
    return "\n".join(lines)
