"""[A] 1단계: 영상·오디오 다운로드 (yt-dlp, FFmpeg)"""
import os
import subprocess

import yt_dlp


def download_video(url, base_dir="data"):
    """유튜브 링크 -> mp4 저장. (video_id, title, video_path, duration) 반환."""
    opts = {
        # 슬라이드 글자를 읽어야 하니 720p 정도로 받음 (너무 크면 처리 느림)
        "format": "bv*[height<=720]+ba/b[height<=720]/b",
        "outtmpl": os.path.join(base_dir, "%(id)s", "video.%(ext)s"),
        "merge_output_format": "mp4",
        "quiet": True,
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
    vid = info["id"]
    video_path = os.path.join(base_dir, vid, "video.mp4")
    return vid, info.get("title", ""), video_path, float(info.get("duration") or 0)


def extract_audio(video_path, audio_path):
    """mp4 -> 16kHz 모노 wav (Whisper 입력 형식)."""
    subprocess.run(
        ["ffmpeg", "-y", "-i", video_path, "-vn", "-ac", "1", "-ar", "16000", audio_path],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    return audio_path
