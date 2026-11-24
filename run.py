"""전체 파이프라인 한 번에 실행: python run.py <유튜브 링크>"""
import sys

from app.export_docx import export_docx
from common import load_json
from speech.pipeline import run as run_b
from video.pipeline import run as run_a

if __name__ == "__main__":
    url = sys.argv[1]
    slides_json = run_a(url)
    print("[A] 완료:", slides_json)
    notes_json = run_b(slides_json)
    print("[B] 완료:", notes_json)
    data = load_json(notes_json)
    out = export_docx(data, notes_json.replace("notes.json", "lecture_notes.docx"))
    print("[C] 완료:", out)
