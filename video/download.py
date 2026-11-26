"""[A] 영상 다운로드 모듈 (#4)"""
from common.schema import VideoMeta


def download(url: str, base_dir: str = "data") -> VideoMeta:
    """YouTube URL -> 영상(mp4) + 오디오(16kHz mono wav) 저장 후 VideoMeta 반환

    입력:  url       예) "https://www.youtube.com/watch?v=..."
    출력:  VideoMeta  video_path = f"{base_dir}/{video_id}/video.mp4"
                      audio_path = f"{base_dir}/{video_id}/audio.wav"
    샘플:  docs/samples/contract/video_meta.json
    힌트:  yt-dlp (다운로드), FFmpeg (-ac 1 -ar 16000)
    """
    raise NotImplementedError("#4")
