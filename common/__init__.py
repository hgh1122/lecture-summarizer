"""팀 공용 함수 (JSON 읽기/쓰기, 시간 표시)."""
import json
import os


def save_json(data, path):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def fmt_time(sec):
    """95.3 -> '00:01:35' (화면 표시용, 데이터는 항상 초 단위)."""
    sec = int(sec)
    return f"{sec // 3600:02d}:{sec % 3600 // 60:02d}:{sec % 60:02d}"
