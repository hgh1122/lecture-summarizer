# 슬라이드 인식 기반 강의 영상 자동 요약기

강의 영상 링크 요청 시 **슬라이드 이미지 + 슬라이드 글자 + 슬라이드 중 발화자 음성 + 요약**으로 카테고리화 기능을 수행하는 프로그램. 

## 업무

| 역할 | 담당 | 폴더 | 한 줄 설명 |
|---|---|---|---|
| A · 영상·화면 | ghhan | `video/` | 영상 취득 및 슬라이드 판별, 글자 인식 |
| B · 음성·텍스트 | ghchoi | `speech/` | STT 구현, 슬라이드별 STT 요약 |
| C · 화면·결과물 | jbkim | `app/` | 결과 화면 송출, Word 변환 |

## 파이프라인 기획

```
URL ─▶ [A] download → slides(전환 감지·캡처) → ocr ─▶ slides.json
                     └▶ extract_audio ───────────────▶ audio.wav
slides.json + audio.wav ─▶ [B] stt → align(슬라이드별 묶기) → summarize ─▶ notes.json
notes.json ─▶ [C] Gradio 화면 / Word 내보내기
```

## 개발 단계

| 1단계 링크 → 슬라이드 캡처·OCR → 자막 → 슬라이드별 원문 노트 화면 
| 2단계 슬라이드별 요약, 중복 슬라이드 제거, 긴 영상 분할, Word 내보내기 
| 3단계  로컬 파일 업로드, 키워드, 검색, .srt 자막 

## Git 규칙

- `main`에 직접 push 금지
- 작업은 `feature/<이름>-<기능>` 브랜치에서 (예: 'feature/ghhan-slide-detect, feature/ghchoi-stt, feature/jbkim-gradio-ui')
- 기능 구현 1가지당 1브랜치, 작업 공간 분리 철저
- Main 브랜치 PR(Pull Request, 브랜치 병합) 은 팀장 확인 후 머지
- 커밋 메시지: `[A] 슬라이드 전환 감지 추가` 처럼 역할 태그를 앞에
- `data/` 폴더(영상, 음성, 결과물같은 대용량 폴더)는 git에 올리지 않음

## 사용할 오픈소스

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
