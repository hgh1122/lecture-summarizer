"""[C] Word 강의 노트 내보내기 (python-docx)

입력:  LectureResult  ->  출력: .docx 파일 경로
구성:  강의 제목 / 전체 요약 / 슬라이드마다 [소제목(시간) -> 슬라이드 이미지 -> 요약 -> 원문]
       (README 모듈 계약: export_docx(result) -> .docx)

검증 (프로젝트 맨 위 폴더에서):
    python -m app.export_docx        ->  data/sample/lecture_notes.docx
"""
import os

from docx import Document
from docx.shared import Inches, Pt, RGBColor

from common import fmt_time
from common.schema import LectureResult

GRAY = RGBColor(0x6E, 0x73, 0x78)   # 원문·보조 글자 색


def slide_title(ocr_text: str, no: int) -> str:
    """슬라이드 제목 = OCR 글자의 첫 줄 (글자가 없으면 '슬라이드 N')"""
    first = (ocr_text or "").strip().split("\n")[0].strip()
    return first or f"슬라이드 {no}"


def export_docx(result: LectureResult, out_path: str | None = None) -> str:
    """LectureResult 를 Word 강의 노트로 저장하고 파일 경로를 돌려준다.

    out_path 를 안 주면 data/<video_id>/lecture_notes.docx 에 저장 (data/ 는 git 에 안 올라감)
    """
    if out_path is None:
        out_path = os.path.join("data", result.meta.video_id, "lecture_notes.docx")
    notes = {n.slide_no: n for n in result.notes}       # slide_no 로 노트 찾기

    doc = Document()
    doc.styles["Normal"].font.size = Pt(11)

    # 1) 강의 정보 (강의당 1번)
    doc.add_heading(result.meta.title or "강의 노트", level=0)
    info = doc.add_paragraph(f"강의 길이 {fmt_time(result.meta.duration)}, 슬라이드 {len(result.slides)}장")
    info.runs[0].font.color.rgb = GRAY
    if result.overview:
        p = doc.add_paragraph()
        p.add_run("전체 요약: ").bold = True
        p.add_run(result.overview)

    # 2) 슬라이드별 노트 (시간 순서)
    for s in result.slides:
        n = notes.get(s.no)
        doc.add_heading(f"{s.no}. {slide_title(s.ocr_text, s.no)}  ({fmt_time(s.start)} ~ {fmt_time(s.end)})", level=1)

        if s.image_path and os.path.exists(s.image_path):
            doc.add_picture(s.image_path, width=Inches(5.5))
        else:
            doc.add_paragraph("(슬라이드 이미지 없음)").runs[0].font.color.rgb = GRAY

        if n and n.summary:
            p = doc.add_paragraph()
            p.add_run("요약: ").bold = True
            p.add_run(n.summary)

        if n and n.keywords:
            p = doc.add_paragraph()
            p.add_run("키워드: ").bold = True
            p.add_run(", ".join(n.keywords))

        p = doc.add_paragraph()
        p.add_run("원문: ").bold = True
        run = p.add_run(n.transcript if n and n.transcript else "(이 슬라이드에서는 말한 내용이 없음)")
        run.font.color.rgb = GRAY

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    doc.save(out_path)
    return out_path


if __name__ == "__main__":
    from common.schema import load_result
    r = load_result("docs/samples/contract/result.json")
    print(export_docx(r))
