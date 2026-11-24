"""[B] 1단계: 슬라이드별로 자막 묶기"""


def align(slides, segments):
    """자막 문장의 가운데 시점이 슬라이드 구간 안에 있으면 그 슬라이드에 넣음."""
    notes = []
    for sl in slides:
        texts = [seg["text"] for seg in segments
                 if sl["start"] <= (seg["start"] + seg["end"]) / 2 < sl["end"]]
        first_line = sl["ocr_text"].split("\n")[0].strip() if sl["ocr_text"] else ""
        notes.append({
            **sl,
            "title": first_line or f"슬라이드 {sl['no']}",
            "transcript": " ".join(texts),
            "summary": "",      # 2단계 summarize에서 채움
            "keywords": [],     # 3단계
        })
    return notes
