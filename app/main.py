"""[C] 강의 노트 웹 UI (#9) — FastAPI + Jinja2

실행 (프로젝트 맨 위 폴더에서):
    uvicorn app.main:app --reload        ->  http://127.0.0.1:8000
    (또는 python -m app.main)

화면
    GET  /                      URL 입력 폼 + 처리 진행 상태
    GET  /sample                샘플 데이터(docs/samples/contract/result.json) 노트 화면
    GET  /lectures/{video_id}   저장된 강의(#8 load_result) 노트 화면
API
    POST /api/jobs              {"url": "..."} -> 처리 시작, job_id 반환
    GET  /api/jobs/{job_id}     진행 상태 조회 (화면이 몇 초마다 물어봄 = 폴링)
    GET  /files/{path}          슬라이드 이미지 (data/, docs/samples/ 아래만 허용)

1단계 메모
- 진행 상태는 서버 메모리에 보관한다. Redis + Celery(작업 큐)가 들어오면 그쪽으로 옮긴다.
- 처리는 한 번에 하나씩만 돌린다 (README: GPU 를 쓰는 단계가 동시에 돌지 않게).
"""
import os
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from threading import Lock

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from common import fmt_time
from common.schema import LectureResult, load_result as load_result_json

ROOT = Path(__file__).resolve().parent.parent          # 프로젝트 맨 위 폴더
SAMPLE = ROOT / "docs/samples/contract/result.json"
ALLOWED_DIRS = [ROOT / "data", ROOT / "docs/samples"]   # 이미지로 내보내도 되는 폴더

app = FastAPI(title="강의 영상 요약기")
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))
templates.env.filters["fmt_time"] = fmt_time           # 템플릿에서 {{ 95.3 | fmt_time }} -> 00:01:35

# ------------------------------------------------------------ 백그라운드 작업
executor = ThreadPoolExecutor(max_workers=1)           # 동시에 1개만 처리
jobs: dict[str, dict] = {}                             # job_id -> {status, message, video_id}
jobs_lock = Lock()


def _set_job(job_id: str, **fields):
    with jobs_lock:
        jobs[job_id].update(fields)


def _run_job(job_id: str, url: str):
    """실제 처리: pipeline.process_lecture (다운로드 → 슬라이드 → 음성 → 정렬 → 요약 → 저장)"""
    _set_job(job_id, status="running", message="처리 중 (다운로드 → 슬라이드 인식 → 음성 인식 → 요약 → 저장)")
    try:
        from pipeline import process_lecture           # 무거운 모듈이라 실제로 처리할 때 불러옴
        result = process_lecture(url)
        _set_job(job_id, status="done", message="완료", video_id=result.meta.video_id)
    except NotImplementedError as e:
        _set_job(job_id, status="failed", message=f"아직 구현되지 않은 단계가 있습니다 ({e})")
    except Exception as e:                             # 어떤 에러든 화면에 이유를 보여줌
        _set_job(job_id, status="failed", message=f"{type(e).__name__}: {e}")


class JobRequest(BaseModel):
    url: str


@app.post("/api/jobs")
def create_job(req: JobRequest):
    url = req.url.strip()
    if not url.startswith(("http://", "https://")):
        raise HTTPException(400, "유튜브 링크(http/https)를 입력해 주세요.")
    job_id = uuid.uuid4().hex[:12]
    with jobs_lock:
        waiting = sum(j["status"] in ("queued", "running") for j in jobs.values())
        jobs[job_id] = {"status": "queued", "message": f"대기 중 (앞에 {waiting}개)", "video_id": None}
    executor.submit(_run_job, job_id, url)
    return {"job_id": job_id}


@app.get("/api/jobs/{job_id}")
def get_job(job_id: str):
    with jobs_lock:
        job = jobs.get(job_id)
        if job is None:
            raise HTTPException(404, "없는 작업입니다.")
        return dict(job)


# ------------------------------------------------------------ 화면
def _view(result: LectureResult) -> list[dict]:
    """슬라이드와 노트를 slide_no 로 짝지어 템플릿에 넘길 목록으로"""
    notes = {n.slide_no: n for n in result.notes}
    rows = []
    for s in result.slides:
        n = notes.get(s.no)
        title = (s.ocr_text or "").strip().split("\n")[0].strip() or f"슬라이드 {s.no}"
        rows.append({"slide": s, "title": title,
                     "transcript": n.transcript if n else "", "summary": n.summary if n else ""})
    return rows


def _render_lecture(request: Request, result: LectureResult, is_sample: bool = False):
    return templates.TemplateResponse(request, "lecture.html", {
        "result": result, "rows": _view(result), "is_sample": is_sample,
    })


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(request, "index.html", {})


@app.get("/sample", response_class=HTMLResponse)
def sample(request: Request):
    """A·B·DB 없이도 화면을 확인할 수 있는 샘플 (이슈 #9 '샘플 데이터 렌더링 검증')"""
    return _render_lecture(request, load_result_json(str(SAMPLE)), is_sample=True)


@app.get("/lectures/{video_id}", response_class=HTMLResponse)
def lecture(request: Request, video_id: str):
    from app.storage import load_result                # #8 저장 모듈
    try:
        result = load_result(video_id)
    except KeyError:
        raise HTTPException(404, f"저장된 강의가 없습니다: {video_id}")
    except NotImplementedError:
        raise HTTPException(503, "저장 모듈(#8)이 아직 main 에 들어오지 않았습니다.")
    return _render_lecture(request, result)


@app.get("/files/{path:path}")
def files(path: str):
    """슬라이드 이미지 전달. ../ 같은 경로로 다른 폴더를 못 읽게 허용 폴더 안인지 확인"""
    target = (ROOT / path).resolve()
    if not any(target.is_relative_to(d.resolve()) for d in ALLOWED_DIRS) or not target.is_file():
        raise HTTPException(404, "파일이 없습니다.")
    return FileResponse(target)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
