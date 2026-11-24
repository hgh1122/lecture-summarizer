#!/usr/bin/env bash
# GitHub 라벨 · 마일스톤 · 이슈를 한 번에 만드는 스크립트
# 준비: GitHub CLI 설치 후 `gh auth login`, 레포 폴더 안에서 실행
#   bash scripts/setup_github.sh
# 아래 세 줄에 팀원 GitHub 아이디를 넣으면 담당자도 자동 지정됨 (비워 두면 라벨만 붙음)
A_USER=""   # 한건희
B_USER=""   # B 담당
C_USER=""   # C 담당

set -e
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
echo "대상 레포: $REPO"

# ---------- 라벨 ----------
lbl() { gh label create "$1" --color "$2" --description "$3" --force >/dev/null; }
lbl "A-영상화면"   "F26B4B" "A · 영상·화면 처리 (video/)"
lbl "B-음성텍스트" "3B82F6" "B · 음성·텍스트 처리 (speech/)"
lbl "C-화면결과물" "059669" "C · 화면·결과물 (app/)"
lbl "필수"        "374151" "1·2단계 필수 기능"
lbl "선택"        "8B3FD1" "3단계, 시간이 남으면"
lbl "통합"        "F2A20C" "모듈 연결 · 공통 작업"

# ---------- 마일스톤 ----------
ms() { gh api "repos/$REPO/milestones" -f title="$1" -f description="$2" >/dev/null 2>&1 || true; }
ms "1단계 최소 완성" "링크 → 슬라이드 캡처·OCR → 자막 → 슬라이드별 원문 노트 화면 (4일차)"
ms "2단계 기본 완성" "요약, 중복 제거, 긴 영상 분할, Word 내보내기 (6일차)"
ms "3단계 추가"      "로컬 업로드, 키워드, 검색, .srt (남는 시간)"

# ---------- 이슈 ----------
# issue <역할> <담당아이디> <마일스톤> <필수|선택> <제목> <본문>
issue() {
  local args=(--title "[$1] $5" --body "$6" --label "$4" --milestone "$3")
  case $1 in A) args+=(--label "A-영상화면");; B) args+=(--label "B-음성텍스트");; C) args+=(--label "C-화면결과물");; 공통) args+=(--label "통합");; esac
  [ -n "$2" ] && args+=(--assignee "$2")
  gh issue create "${args[@]}" >/dev/null && echo "  + [$1] $5"
}
M1="1단계 최소 완성"; M2="2단계 기본 완성"; M3="3단계 추가"

echo "이슈 생성 중..."
issue 공통 "" "$M1" 필수 "개발 환경 설치 확인 (3명 모두)" \
"- [ ] Python 3.11, FFmpeg, Ollama 설치
- [ ] \`pip install -r requirements.txt\` 성공
- [ ] \`python -m app.main\` → 샘플 데이터로 보기 동작
- [ ] 각자 GPU 유무 / VRAM 댓글로 남기기"

issue A "$A_USER" "$M1" 필수 "영상·오디오 다운로드" \
"파일: \`video/download.py\`
- [ ] 유튜브 링크 → \`data/<id>/video.mp4\`
- [ ] mp4 → 16kHz 모노 \`audio.wav\`
- [ ] 테스트 영상 1개로 확인"

issue A "$A_USER" "$M1" 필수 "슬라이드 전환 감지 + 캡처" \
"파일: \`video/slides.py\`
- [ ] PySceneDetect로 전환 시점 찾기
- [ ] 너무 짧은 구간 합치기
- [ ] 구간 중간 프레임을 png로 저장
- [ ] 테스트 영상에서 threshold 조절 결과 공유"

issue A "$A_USER" "$M1" 필수 "슬라이드 글자 인식 (OCR) + slides.json 출력" \
"파일: \`video/ocr.py\`, \`video/pipeline.py\`
- [ ] EasyOCR 한/영 인식
- [ ] \`docs/interface.md\` 형식대로 \`slides.json\` 저장
- [ ] B에게 실제 slides.json 전달"

issue B "$B_USER" "$M1" 필수 "음성 인식 (faster-whisper)" \
"파일: \`speech/stt.py\`
- [ ] wav → 타임스탬프 자막 리스트
- [ ] small / medium 속도·정확도 비교해서 모델 결정
- [ ] A 결과 전에는 아무 강의 wav로 테스트"

issue B "$B_USER" "$M1" 필수 "슬라이드별 자막 묶기 + notes.json 출력" \
"파일: \`speech/align.py\`, \`speech/pipeline.py\`
- [ ] \`docs/samples/slides.json\`(샘플)으로 먼저 개발
- [ ] \`docs/interface.md\` 형식대로 \`notes.json\` 저장
- [ ] C에게 실제 notes.json 전달"

issue C "$C_USER" "$M1" 필수 "웹 화면 + 슬라이드 노트 화면 (Gradio)" \
"파일: \`app/main.py\`
- [ ] 샘플 데이터로 화면 구성 다듬기
- [ ] 진행 상황 표시
- [ ] 슬라이드 이미지 · 제목 · 시간 · 설명이 한눈에 보이게"

issue 공통 "" "$M1" 필수 "1단계 통합 테스트 (3일차 중간 점검)" \
"- [ ] \`python run.py <테스트 영상>\` 끝까지 실행
- [ ] 막힌 부분 정리"

issue A "$A_USER" "$M2" 필수 "중복 슬라이드 제거" \
"파일: \`video/slides.py\` remove_duplicates
- [ ] 이미지 차이 또는 OCR 글자 유사도로 연속 중복 합치기"

issue A "$A_USER" "$M2" 필수 "긴 영상 분할" \
"파일: \`video/split.py\`
- [ ] 10분 단위 오디오 분할 + 시간 offset 전달
- [ ] B와 연결 방식 협의"

issue B "$B_USER" "$M2" 필수 "슬라이드별 요약 (Ollama)" \
"파일: \`speech/summarize.py\`
- [ ] 사용할 로컬 모델 결정 (팀원 사양 고려)
- [ ] 프롬프트 다듬기, 지어내는 내용 없는지 확인"

issue C "$C_USER" "$M2" 필수 "Word 강의 노트 내보내기" \
"파일: \`app/export_docx.py\`
- [ ] 슬라이드 이미지 + 요약 + 원문
- [ ] 목차, 서식 다듬기"

issue A "$A_USER" "$M3" 선택 "로컬 녹화 파일 업로드 처리" "- [ ] mp4 파일을 직접 넣어도 slides.json 생성"
issue B "$B_USER" "$M3" 선택 "키워드 추출" "- [ ] 슬라이드별 핵심 용어 → notes[].keywords"
issue B "$B_USER" "$M3" 선택 "강의 내용 검색 로직" "- [ ] sentence-transformers 임베딩으로 질문과 비슷한 구간 찾기"
issue C "$C_USER" "$M3" 선택 ".srt 자막 내보내기" "- [ ] notes.json segments → .srt"
issue C "$C_USER" "$M3" 선택 "검색창 화면" "- [ ] 검색 결과 클릭하면 해당 슬라이드로 이동"

echo "완료! https://github.com/$REPO/issues"
