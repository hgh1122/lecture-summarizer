"""[C] 2단계: Word 강의 노트 내보내기 (python-docx)"""
import os

from docx import Document
from docx.shared import Inches

from common import fmt_time


def export_docx(notes_data, out_path):
    doc = Document()
    doc.add_heading(notes_data["title"] or "강의 노트", level=0)
    for n in notes_data["notes"]:
        doc.add_heading(f"{n['no']}. {n['title']}  ({fmt_time(n['start'])} ~ {fmt_time(n['end'])})", level=1)
        if n.get("image") and os.path.exists(n["image"]):
            doc.add_picture(n["image"], width=Inches(5.5))
        if n.get("summary"):
            p = doc.add_paragraph()
            p.add_run("요약: ").bold = True
            p.add_run(n["summary"])
        if n.get("transcript"):
            doc.add_paragraph(n["transcript"])
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    doc.save(out_path)
    return out_path
