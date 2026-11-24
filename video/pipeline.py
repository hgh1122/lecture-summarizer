"""[A] 전체 흐름: URL -> slides.json  (A → B 인터페이스: docs/interface.md)"""
import os

from common import save_json
from video.download import download_video, extract_audio
from video.ocr import read_text
from video.slides import capture_slides, detect_slides, remove_duplicates


def run(url, base_dir="data"):
    vid, title, video_path, duration = download_video(url, base_dir)
    work = os.path.join(base_dir, vid)
    audio_path = extract_audio(video_path, os.path.join(work, "audio.wav"))

    ranges = detect_slides(video_path)
    images = capture_slides(video_path, ranges, os.path.join(work, "slides"))
    slides = [
        {"no": i, "start": round(s, 2), "end": round(e, 2), "image": img, "ocr_text": read_text(img)}
        for i, ((s, e), img) in enumerate(zip(ranges, images), 1)
    ]
    slides = remove_duplicates(slides)

    data = {"video_id": vid, "title": title, "video_path": video_path,
            "audio_path": audio_path, "duration": duration, "slides": slides}
    out = os.path.join(work, "slides.json")
    save_json(data, out)
    return out
