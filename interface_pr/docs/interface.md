# 모듈 인터페이스

모듈 간 데이터 형식의 기준은 **`common/schema.py`** 입니다. 이 문서는 요약본입니다.

## 규칙
- 모든 모듈은 `common/schema.py`의 데이터 클래스로만 입력/출력을 주고받습니다.
- 시간 값은 모두 **초(float)** 단위입니다.
- `schema.py` 변경은 별도 PR로 올리고, 팀원 전원 리뷰 후 머지합니다.

## 함수 시그니처

| 모듈 | 담당 | 함수 | 입력 → 출력 | 이슈 |
|---|---|---|---|---|
| 다운로드 | A | `video.download.download(url)` | `str` → `VideoMeta` | #4 |
| 슬라이드 | A | `video.slides.extract_slides(video_path)` | `str` → `list[Slide]` | #5 |
| 음성 인식 | B | `speech.stt.transcribe(audio_path)` | `str` → `list[Segment]` | #6 |
| 정렬 | B | `speech.align.align(slides, segments)` | `list[Slide], list[Segment]` → `list[Note]` | #7 |
| 요약 | B | `speech.summarize.summarize(slides, notes)` | → `(list[Note], str)` | 2단계 |
| 저장 | C | `app.storage.save_result / load_result` | `LectureResult` ↔ 저장소 | #8 |
| 웹 UI | C | `app/` | `LectureResult` → 화면 | #9 |
| 통합 | 공통 | `pipeline.process_lecture(url)` | `str` → `LectureResult` | #10 |

## 샘플 데이터 (`docs/samples/contract/`)

| 파일 | 형식 | 용도 |
|---|---|---|
| `video_meta.json` | `VideoMeta` | download 출력 예시 |
| `slides.json` | `list[Slide]` | extract_slides 출력 / align 입력 |
| `segments.json` | `list[Segment]` | transcribe 출력 / align 입력 |
| `notes.json` | `list[Note]` | align 출력 (정답 예시) |
| `result.json` | `LectureResult` | 저장·웹 UI 입력 |

앞 단계가 완성되지 않았어도 샘플을 불러와 개발할 수 있습니다.

```python
from common.schema import load_slides, load_segments, load_result
slides = load_slides("docs/samples/contract/slides.json")
segments = load_segments("docs/samples/contract/segments.json")
result = load_result("docs/samples/contract/result.json")
```

샘플 검증: `python -m common.schema`
