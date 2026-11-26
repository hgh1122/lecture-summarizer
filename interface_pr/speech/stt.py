"""[B] 음성 인식 모듈 (#6)"""
from common.schema import Segment


def transcribe(audio_path: str, language: str = "ko") -> list[Segment]:
    """오디오(16kHz mono wav) -> 타임스탬프가 붙은 발화 구간

    입력:  audio_path  VideoMeta.audio_path
    출력:  list[Segment] (start, end 초 단위, text)
    샘플:  docs/samples/contract/segments.json
    힌트:  faster-whisper (WhisperModel, vad_filter=True)
    """
    raise NotImplementedError("#6")
