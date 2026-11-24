"""[B] 2단계: 슬라이드별 요약 (Ollama 로컬 LLM)"""
import ollama

MODEL = "qwen2.5:3b"  # 팀에서 정한 모델로 교체 (ollama pull <모델>)

PROMPT = """다음은 강의 슬라이드 하나의 내용과, 그 슬라이드를 설명하며 강사가 한 말이다.
핵심 내용을 한국어 2~3문장으로 요약하라. 없는 내용은 지어내지 마라.

[슬라이드 글자]
{ocr}

[강사 설명]
{transcript}
"""


def summarize_note(note):
    if not note["transcript"].strip():
        return ""
    try:
        res = ollama.chat(model=MODEL, messages=[{"role": "user", "content": PROMPT.format(
            ocr=note["ocr_text"], transcript=note["transcript"])}])
        return res["message"]["content"].strip()
    except Exception as e:  # Ollama가 꺼져 있어도 전체가 멈추지 않게
        print("[summarize] 실패:", e)
        return ""


def summarize_all(notes):
    for n in notes:
        n["summary"] = summarize_note(n)
    return notes
