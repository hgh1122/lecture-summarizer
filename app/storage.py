"""[C] 결과 저장 모듈 (#8)

LectureResult 를 PostgreSQL 의 lectures / slides / notes 테이블에 저장하고 다시 꺼낸다.

DB 띄우기 (Docker, 처음 한 번):
    docker run -d --name opensw-db -p 5432:5432 \
        -e POSTGRES_USER=opensw -e POSTGRES_PASSWORD=opensw -e POSTGRES_DB=opensw \
        -v opensw-pgdata:/var/lib/postgresql/data postgres:17
접속 주소는 환경변수 DATABASE_URL 로 바꿀 수 있음 (기본값은 위 컨테이너 기준)
검증: python -m app.storage
"""
import os

from common.schema import LectureResult, Note, Slide, VideoMeta

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://opensw:opensw@localhost:5432/opensw"
)

# 테이블 설계: 강의 1 : 슬라이드 N : 노트 N  (video_id 로 연결)
# - end 는 SQL 예약어라 start_sec / end_sec 로 이름 붙임
# - 시간은 초 단위 실수 -> DOUBLE PRECISION (REAL 은 95.3 이 95.30000305 로 바뀜)
# - 강의를 지우면 그 강의의 슬라이드·노트도 같이 지워짐 (ON DELETE CASCADE)
SCHEMA = """
CREATE TABLE IF NOT EXISTS lectures (
    video_id   TEXT PRIMARY KEY,
    title      TEXT NOT NULL,
    video_path TEXT,
    audio_path TEXT,
    duration   DOUBLE PRECISION,
    overview   TEXT NOT NULL DEFAULT '',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS slides (
    video_id   TEXT NOT NULL REFERENCES lectures(video_id) ON DELETE CASCADE,
    no         INTEGER NOT NULL,
    start_sec  DOUBLE PRECISION NOT NULL,
    end_sec    DOUBLE PRECISION NOT NULL,
    image_path TEXT,
    ocr_text   TEXT NOT NULL DEFAULT '',
    PRIMARY KEY (video_id, no)
);
CREATE TABLE IF NOT EXISTS notes (
    video_id   TEXT NOT NULL REFERENCES lectures(video_id) ON DELETE CASCADE,
    slide_no   INTEGER NOT NULL,
    transcript TEXT NOT NULL DEFAULT '',
    summary    TEXT NOT NULL DEFAULT '',
    keywords   TEXT[] NOT NULL DEFAULT '{}',
    PRIMARY KEY (video_id, slide_no)
);
"""


def _connect():
    """DB 연결 + 테이블이 없으면 생성"""
    import psycopg  # 여기서 import: DB 안 쓰는 팀원은 psycopg 없어도 pipeline import 가능

    conn = psycopg.connect(DATABASE_URL)
    conn.execute(SCHEMA)
    conn.commit()
    return conn


def save_result(result: LectureResult) -> None:
    """처리 결과 저장 (lectures / slides / notes)

    입력:  LectureResult
    샘플:  docs/samples/contract/result.json
    같은 video_id 를 다시 저장하면 이전 결과를 지우고 새로 덮어쓴다.
    """
    m = result.meta
    with _connect() as conn:  # with 블록 = 트랜잭션: 끝나면 commit, 에러 나면 전부 rollback
        conn.execute("DELETE FROM lectures WHERE video_id = %s", (m.video_id,))
        conn.execute(
            "INSERT INTO lectures (video_id, title, video_path, audio_path, duration, overview)"
            " VALUES (%s, %s, %s, %s, %s, %s)",
            (m.video_id, m.title, m.video_path, m.audio_path, m.duration, result.overview),
        )
        with conn.cursor() as cur:
            cur.executemany(
                "INSERT INTO slides (video_id, no, start_sec, end_sec, image_path, ocr_text)"
                " VALUES (%s, %s, %s, %s, %s, %s)",
                [(m.video_id, s.no, s.start, s.end, s.image_path, s.ocr_text) for s in result.slides],
            )
            cur.executemany(
                "INSERT INTO notes (video_id, slide_no, transcript, summary, keywords)"
                " VALUES (%s, %s, %s, %s, %s)",
                [(m.video_id, n.slide_no, n.transcript, n.summary, n.keywords) for n in result.notes],
            )


def load_result(video_id: str) -> LectureResult:
    """저장된 결과 조회 -> LectureResult (없으면 KeyError)"""
    with _connect() as conn:
        row = conn.execute(
            "SELECT video_id, title, video_path, audio_path, duration, overview"
            " FROM lectures WHERE video_id = %s", (video_id,),
        ).fetchone()
        if row is None:
            raise KeyError(f"저장된 강의 없음: {video_id}")
        slides = [Slide(*r) for r in conn.execute(
            "SELECT no, start_sec, end_sec, image_path, ocr_text"
            " FROM slides WHERE video_id = %s ORDER BY no", (video_id,))]
        notes = [Note(*r) for r in conn.execute(
            "SELECT slide_no, transcript, summary, keywords"
            " FROM notes WHERE video_id = %s ORDER BY slide_no", (video_id,))]
    return LectureResult(VideoMeta(*row[:5]), slides, notes, row[5])


if __name__ == "__main__":
    # 샘플 데이터 저장 -> 조회 -> 원본과 비교
    from common.schema import load_result as load_json_result

    sample = load_json_result("docs/samples/contract/result.json")
    save_result(sample)
    loaded = load_result(sample.meta.video_id)
    print("슬라이드", len(loaded.slides), "개 / 노트", len(loaded.notes), "개")
    print("원본과 동일:", loaded == sample)
