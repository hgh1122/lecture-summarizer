"""[B] 1단계: 음성 인식 (faster-whisper)"""
from faster_whisper import WhisperModel

MODEL_SIZE = "small"  # 사양 되면 "medium" 또는 "large-v3-turbo"
_model = None


def transcribe(audio_path, language="ko"):
    """wav -> [{"start", "end", "text"}, ...] (초 단위)."""
    global _model
    if _model is None:
        _model = WhisperModel(MODEL_SIZE, device="auto", compute_type="default")
    segments, _info = _model.transcribe(audio_path, language=language, vad_filter=True)
    return [{"start": round(s.start, 2), "end": round(s.end, 2), "text": s.text.strip()}
            for s in segments]
