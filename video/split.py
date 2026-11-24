"""[A] 2단계: 긴 영상 분할 (FFmpeg) — TODO
목표: 1시간 이상 오디오를 10분 단위로 잘라 B가 나눠서 처리할 수 있게 하기.
힌트: ffmpeg -i audio.wav -f segment -segment_time 600 -c copy out_%03d.wav
주의: 잘린 조각의 시간은 0부터 시작하므로 B에게 넘길 때 offset(초)을 같이 넘겨야 함."""


def split_audio(audio_path, out_dir, chunk_sec=600):
    raise NotImplementedError
