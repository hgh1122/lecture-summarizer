# 슬라이드 인식 기반 강의 영상 자동 요약기

강의 영상 링크를 넣으면 **슬라이드 이미지 + 슬라이드 글자 + 그 시간에 한 말 + 요약**이 한 장씩 묶인 강의 노트를 만들어 주는 프로그램입니다. 모든 모델은 로컬에서 동작합니다.

## 팀원과 역할

| 역할 | 담당 | 폴더 | 한 줄 설명 |
|---|---|---|---|
| A · 영상·화면 | 한건희 | `video/` | 영상을 받아 슬라이드를 찾고 글자를 읽음 |
| B · 음성·텍스트 | [이름] | `speech/` | 말을 글로 바꾸고 슬라이드별로 묶어 요약 |
| C · 화면·결과물 | [이름] | `app/` | 결과를 화면에 보여주고 Word로 내보냄 |

통합(main 머지) 담당: [이름]

## 전체 흐름

```
URL ─▶ [A] download → slides(전환 감지·캡처) → ocr ─▶ slides.json
                     └▶ extract_audio ───────────────▶ audio.wav
slides.json + audio.wav ─▶ [B] stt → align(슬라이드별 묶기) → summarize ─▶ notes.json
notes.json ─▶ [C] Gradio 화면 / Word 내보내기
```

모듈 사이 데이터 형식은 [`docs/interface.md`](docs/interface.md)에 있고, 샘플은 `docs/samples/`에 있습니다.
**앞 단계 결과를 기다리지 말고 샘플 JSON으로 먼저 개발하세요.**

## 개발 단계

| 단계 | 목표 | 기한 |
|---|---|---|
| 1단계 · 최소 완성 | 링크 → 슬라이드 캡처·OCR → 자막 → 슬라이드별 원문 노트 화면 | 4일차 |
| 2단계 · 기본 완성 | 슬라이드별 요약, 중복 슬라이드 제거, 긴 영상 분할, Word 내보내기 | 6일차 |
| 3단계 · 추가 | 로컬 파일 업로드, 키워드, 검색, .srt 자막 | 남는 시간 |

세부 업무는 GitHub Issues에서 확인하세요 (라벨: `A-영상화면`, `B-음성텍스트`, `C-화면결과물`).

## 설치

1. Python 3.11 설치
2. FFmpeg 설치 (Windows: `winget install ffmpeg`, macOS: `brew install ffmpeg`)
3. [Ollama](https://ollama.com) 설치 후 요약 모델 받기: `ollama pull qwen2.5:3b` (모델은 팀에서 정한 것으로)
4. PyTorch 설치 (GPU가 있으면 CUDA 버전에 맞게)
5. 나머지 패키지
   ```bash
   python -m venv .venv
   # Windows: .venv\Scripts\activate   /   macOS·Linux: source .venv/bin/activate
   pip install -r requirements.txt
   ```
6. 설치 확인: `python -m app.main` 을 실행하고 "샘플 데이터로 보기"가 열리면 성공

## 실행

```bash
python run.py "https://www.youtube.com/watch?v=..."   # 전체 파이프라인
python -m app.main                                      # 웹 화면
```

## Git 규칙

- `main`에 직접 push 금지
- 작업은 `feature/<이름>-<기능>` 브랜치에서 (예: `feature/gunhee-slide-detect`)
- Issue 하나 = 브랜치 하나 = PR 하나. PR 설명에 `Closes #이슈번호`
- PR은 팀원 1명 이상 확인 후 머지
- 커밋 메시지: `[A] 슬라이드 전환 감지 추가` 처럼 역할 태그를 앞에
- `data/` 폴더(영상, 음성, 결과물)는 git에 올리지 않음

## 매일 공유 (저녁)

```
오늘 한 것:
막힌 것:
내일 할 것:
```

## 사용 오픈소스

| 오픈소스 | 용도 |
|---|---|
| yt-dlp | 영상·오디오 다운로드 |
| FFmpeg | 오디오 추출·변환, 영상 분할 |
| OpenCV | 프레임 처리, 슬라이드 캡처 |
| PySceneDetect | 슬라이드 전환 감지 |
| EasyOCR | 슬라이드 글자 인식 |
| faster-whisper | 음성 인식 |
| Ollama | 로컬 LLM 요약 |
| PyTorch | 딥러닝 실행 환경 |
| Gradio | 웹 화면 |
| python-docx | Word 강의 노트 생성 |
