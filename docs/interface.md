# 모듈 사이 데이터 형식

- **시간은 모두 초 단위 숫자(float)** 로 주고받습니다. `00:01:35` 같은 표시는 화면(C)에서만 바꿉니다.
- 경로는 프로젝트 루트 기준 상대 경로입니다.
- 형식을 바꾸고 싶으면 이 문서를 고치는 PR을 먼저 올리고 팀원 확인을 받습니다.

## A → B : `data/<영상id>/slides.json`

```json
{
  "video_id": "abc123",
  "title": "강의 제목",
  "video_path": "data/abc123/video.mp4",
  "audio_path": "data/abc123/audio.wav",
  "duration": 1234.5,
  "slides": [
    {"no": 1, "start": 0.0, "end": 95.3, "image": "data/abc123/slides/001.png", "ocr_text": "CNN 개요"}
  ]
}
```

| 키 | 설명 |
|---|---|
| `slides[].no` | 1부터 시작하는 슬라이드 번호 |
| `slides[].start`, `end` | 그 슬라이드가 화면에 떠 있던 구간(초) |
| `slides[].image` | 캡처한 슬라이드 이미지 경로 |
| `slides[].ocr_text` | 슬라이드에서 읽은 글자 (줄바꿈은 `\n`) |

## B → C : `data/<영상id>/notes.json`

```json
{
  "video_id": "abc123",
  "title": "강의 제목",
  "duration": 1234.5,
  "segments": [
    {"start": 0.0, "end": 4.2, "text": "오늘은 CNN을 배웁니다"}
  ],
  "notes": [
    {
      "no": 1, "start": 0.0, "end": 95.3,
      "image": "data/abc123/slides/001.png",
      "ocr_text": "CNN 개요",
      "title": "CNN 개요",
      "transcript": "오늘은 CNN을 배웁니다. ...",
      "summary": "합성곱 신경망의 기본 개념을 소개함",
      "keywords": []
    }
  ]
}
```

| 키 | 설명 |
|---|---|
| `segments` | 음성 인식 원본 결과 (자막 .srt 만들 때 사용) |
| `notes[].title` | 슬라이드 제목 (OCR 첫 줄, 없으면 "슬라이드 N") |
| `notes[].transcript` | 그 슬라이드 구간에 한 말 전체 |
| `notes[].summary` | 요약 (2단계 전까지는 빈 문자열 `""`) |
| `notes[].keywords` | 3단계 기능, 없으면 빈 리스트 |

샘플: [`samples/slides.json`](samples/slides.json), [`samples/notes.json`](samples/notes.json)
