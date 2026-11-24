"""[C] 1단계: 웹 화면 (Gradio)
실행: 프로젝트 루트에서  python -m app.main
'샘플 데이터로 보기'는 A, B 모듈 없이도 동작하므로 C는 이걸로 먼저 개발하면 됨."""
import os

import gradio as gr

from app.export_docx import export_docx
from common import fmt_time, load_json

SAMPLE = "docs/samples/notes.json"


def render(notes_data):
    """notes.json -> (갤러리 [(이미지, 캡션)], 마크다운 노트, docx 경로)"""
    gallery = [(n["image"], f"{n['no']}. {n['title']}")
               for n in notes_data["notes"] if os.path.exists(n["image"])]
    md = [f"# {notes_data['title']}"]
    for n in notes_data["notes"]:
        md.append(f"## {n['no']}. {n['title']}  `{fmt_time(n['start'])} ~ {fmt_time(n['end'])}`")
        if n.get("summary"):
            md.append(f"**요약** {n['summary']}")
        md.append(f"> {n['transcript'] or '(설명 없음)'}")
    docx_path = export_docx(notes_data, os.path.join("data", notes_data["video_id"], "lecture_notes.docx"))
    return gallery, "\n\n".join(md), docx_path


def on_sample():
    return render(load_json(SAMPLE))


def on_run(url, progress=gr.Progress()):
    # A, B 모듈이 완성되면 연결됨 (그 전에는 샘플 버튼으로 개발)
    from video.pipeline import run as run_a
    from speech.pipeline import run as run_b
    progress(0.1, desc="영상 다운로드 · 슬라이드 인식 중 (A)")
    slides_json = run_a(url)
    progress(0.5, desc="음성 인식 · 요약 중 (B)")
    notes_json = run_b(slides_json)
    progress(0.9, desc="노트 만드는 중 (C)")
    return render(load_json(notes_json))


with gr.Blocks(title="강의 영상 요약기") as demo:
    gr.Markdown("# 강의 영상 요약기\n슬라이드와 설명을 묶어 강의 노트를 만들어 줍니다.")
    with gr.Row():
        url = gr.Textbox(label="유튜브 링크", scale=4)
        btn = gr.Button("노트 만들기", variant="primary", scale=1)
        sample_btn = gr.Button("샘플 데이터로 보기", scale=1)
    gallery = gr.Gallery(label="슬라이드", columns=4, height=220)
    notes_md = gr.Markdown()
    docx_file = gr.File(label="Word 강의 노트")

    btn.click(on_run, inputs=url, outputs=[gallery, notes_md, docx_file])
    sample_btn.click(on_sample, outputs=[gallery, notes_md, docx_file])

if __name__ == "__main__":
    demo.launch(allowed_paths=["data", "docs/samples"])
