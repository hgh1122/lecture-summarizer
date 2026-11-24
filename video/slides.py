"""[A] 1단계: 슬라이드 전환 감지 + 캡처 (PySceneDetect, OpenCV)
   [A] 2단계: 중복 슬라이드 제거 (TODO)"""
import os

import cv2
from scenedetect import ContentDetector, detect


def detect_slides(video_path, threshold=27.0, min_len_sec=3.0):
    """화면이 크게 바뀌는 지점으로 구간을 나눔. [(start, end), ...] (초)."""
    scenes = detect(video_path, ContentDetector(threshold=threshold))
    ranges = [(s.get_seconds(), e.get_seconds()) for s, e in scenes]
    if not ranges:  # 전환이 하나도 없으면 영상 전체를 슬라이드 1장으로
        cap = cv2.VideoCapture(video_path)
        dur = cap.get(cv2.CAP_PROP_FRAME_COUNT) / (cap.get(cv2.CAP_PROP_FPS) or 30)
        cap.release()
        ranges = [(0.0, dur)]
    # 너무 짧은 구간(애니메이션, 깜빡임)은 앞 구간에 합침
    merged = []
    for s, e in ranges:
        if merged and e - s < min_len_sec:
            merged[-1] = (merged[-1][0], e)
        else:
            merged.append((s, e))
    return merged


def capture_slides(video_path, ranges, out_dir):
    """각 구간 중간 지점 프레임을 png로 저장. 이미지 경로 리스트 반환."""
    os.makedirs(out_dir, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    paths = []
    for i, (s, e) in enumerate(ranges, 1):
        cap.set(cv2.CAP_PROP_POS_MSEC, (s + e) / 2 * 1000)
        ok, frame = cap.read()
        path = os.path.join(out_dir, f"{i:03d}.png")
        if ok:
            cv2.imwrite(path, frame)
        paths.append(path)
    cap.release()
    return paths


def remove_duplicates(slides):
    """TODO(2단계): 거의 같은 슬라이드가 연속이면 하나로 합치기.
    아이디어: 이전 슬라이드 이미지와 흑백 차이(cv2.absdiff) 평균이 작거나,
    OCR 글자가 거의 같으면 end를 늘리고 현재 슬라이드는 버림."""
    return slides
