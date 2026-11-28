"""[B] 음성 인식 모듈 (#6)"""

import math
import os
from pathlib import Path

import ctranslate2
from faster_whisper import WhisperModel

from common.schema import Segment


# 모델 및 실행 환경 설정
MODEL_SIZE = os.getenv("WHISPER_MODEL", "auto")
DEVICE = os.getenv("WHISPER_DEVICE", "auto")
COMPUTE_TYPE = os.getenv("WHISPER_COMPUTE_TYPE", "auto")

_model = None


def _get_model():
    """Whisper 모델을 최초 한 번만 로딩한다."""
    global _model

    if _model is None:
        device = DEVICE
        compute_type = COMPUTE_TYPE

        # GPU가 있으면 CUDA, 없으면 CPU 사용
        if device == "auto":
            device = (
                "cuda"
                if ctranslate2.get_cuda_device_count() > 0
                else "cpu"
            )

        # 실행 장치에 따른 연산 정밀도 설정
        if compute_type == "auto":
            compute_type = (
                "float16" if device == "cuda" else "int8"
            )

        # 실행 장치에 따른 기본 모델 선택
        model_size = MODEL_SIZE
        if model_size == "auto":
            model_size = "medium" if device == "cuda" else "small"

        print(
            f"[STT] Loading Whisper: {model_size}, "
            f"device={device}, compute_type={compute_type}"
        )

        _model = WhisperModel(
            model_size,
            device=device,
            compute_type=compute_type,
        )

    return _model


def transcribe(
    audio_path: str,
    language: str = "ko"
) -> list[Segment]:
    """음성 파일을 타임스탬프가 포함된 발화 구간으로 변환한다.

    입력:
        audio_path: 음성 파일 경로
        language: 음성 인식 언어

    출력:
        list[Segment]
        start, end: 초 단위 시간
        text: 인식된 발화 내용
    """

    if not Path(audio_path).is_file():
        raise FileNotFoundError(
            f"Audio file not found: {audio_path}"
        )

    model = _get_model()

    segments, info = model.transcribe(
        audio_path,
        language=language,
        vad_filter=True,
        beam_size=5,
    )

    duration = float(info.duration)
    results = []

    for seg in segments:
        text = seg.text.strip()

        if not text:
            continue

        raw_start = float(seg.start)
        raw_end = float(seg.end)

        # 실제 음성 길이 범위로 타임스탬프 보정
        start = max(0.0, raw_start)
        end = min(duration, raw_end)

        if start != raw_start or end != raw_end:
            print(
                f"[STT] Timestamp corrected: "
                f"({raw_start:.4f}, {raw_end:.4f}) -> "
                f"({start:.4f}, {end:.4f})"
            )

        if not (
            math.isfinite(raw_start)
            and math.isfinite(raw_end)
            and 0 <= start < end <= duration
        ):
            print(f"[STT] Invalid segment skipped: {seg}")
            continue

        results.append(
            Segment(
                start=start,
                end=end,
                text=text,
            )
        )

    return results
