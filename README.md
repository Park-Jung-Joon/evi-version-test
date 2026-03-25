# EVIDENCE Versioning Test Environment

Changepacks 기반 유의적 버저닝(Semantic Versioning) 테스트 환경.

## 구조

```
evi_version_test/
├── .changepacks/
│   └── config.json              # changepacks 설정
├── .github/workflows/
│   ├── pr-changepacks-check.yaml   # dev PR 시 changepacks JSON 존재 확인
│   ├── version-update.yaml         # main merge 시 버전 자동 업데이트 + 태그
│   └── scheduled-merge.yaml        # 정기 dev→main 자동 머지
├── evidence_snv/
│   ├── pyproject.toml           # evidence-snv 패키지 (evidence 버전 공유)
│   └── main.py                  # SNV 분석 데모
├── evidence_cnv/
│   ├── pyproject.toml           # evidence-cnv 패키지 (evidence 버전 공유)
│   └── main.py                  # CNV 분석 데모
├── pipeline/
│   ├── pyproject.toml           # pipeline 패키지
│   └── main.py                  # 파이프라인 오케스트레이션 데모
├── genet/                       # (범위 외, ignore 대상)
├── scripts/
│   └── sync_version.py          # pyproject.toml → version.py 동기화
└── version.py                   # 최종 버전 관리 파일
```

## 패키지 버전 정책

| 패키지 | 구성 디렉토리 | 버전 동기화 |
|--------|--------------|------------|
| **evidence** | evidence_snv, evidence_cnv | 둘 중 하나라도 변경 시 동일 버전으로 업데이트 |
| **pipeline** | pipeline | 독립 버전 관리 |

`updateOn` 설정으로 evidence_snv ↔ evidence_cnv 버전이 자동 동기화됩니다.

## 브랜치 전략

```
main          ← 운영 배포. 직접 Push 금지. 버전 태그 자동 생성.
  ↑ merge (weekly / scheduled)
dev           ← 통합 개발. changepacks JSON이 누적됨.
  ↑ merge (PR)
feat/작업명    ← 개인 작업 브랜치
```

## 사전 준비

```bash
# cy2 서버에서 changepacks 설치
pip install changepacks

# (선택) changepacks init - 이미 .changepacks/config.json이 있으므로 건너뛰어도 됨
changepacks init
```

---

## 테스트 시나리오

### 시나리오 1: evidence_snv 변경 → evidence 버전 업

evidence_snv에 새 기능을 추가하고 Minor 버전을 올리는 시나리오.

```bash
# 1. dev에서 feature 브랜치 생성
git checkout dev
git checkout -b feat/snv-quality-filter

# 2. evidence_snv/main.py에 기능 추가
#    (예: filter_by_quality 함수 추가)

# 3. changepacks 실행 → evidence-snv 선택 → Minor → 노트 작성
changepacks

# 4. 커밋 & push
git add -A
git commit -m "feat: SNV quality filter 기능 추가"
git push -u origin feat/snv-quality-filter

# 5. GitHub에서 dev로 PR 생성 → changepacks check 통과 확인 → merge

# 6. dev → main 머지 시 CI가 자동으로:
#    - changepacks update 실행
#    - evidence_snv + evidence_cnv 모두 v1.1.0으로 업데이트
#    - version.py의 EVIDENCE_VERSION = "v1.1.0"으로 갱신
#    - evidence-v1.1.0 태그 생성
```

**확인 포인트:**
- evidence_cnv도 동일 버전(v1.1.0)으로 동기화 되는지
- version.py의 EVIDENCE_VERSION이 변경되는지
- PIPELINE_VERSION은 변경되지 않는지

### 시나리오 2: pipeline 변경 → pipeline 버전 업

```bash
# 1. dev에서 feature 브랜치 생성
git checkout dev
git pull origin dev
git checkout -b feat/pipeline-qc-step

# 2. pipeline/main.py에 기능 추가
#    (예: run_qc_step 함수 추가)

# 3. changepacks 실행 → pipeline 선택 → Patch → 노트 작성
changepacks

# 4. 커밋 & push → PR → dev 머지 → main 머지
git add -A
git commit -m "feat: pipeline QC step 추가"
git push -u origin feat/pipeline-qc-step

# 5. CI가 자동으로 pipeline v1.0.1 업데이트, 태그 생성
```

**확인 포인트:**
- PIPELINE_VERSION만 v1.0.1로 변경되는지
- EVIDENCE_VERSION은 이전 값 유지하는지

### 시나리오 3: 정기 자동 머지 (Scheduled Merge)

```bash
# scheduled-merge.yaml이 30분마다 실행됨.
# dev에 changepacks JSON이 있으면 자동으로 dev→main PR 생성.
# 수동 실행도 가능: GitHub Actions → Scheduled Dev to Main Merge → Run workflow
```

**확인 포인트:**
- dev에 changepack_log_*.json이 있을 때만 PR 생성되는지
- 이미 열린 PR이 있으면 중복 생성하지 않는지

### 시나리오 4: 핫픽스

main에서 긴급 수정 후 dev로 역머지하는 시나리오.

```bash
# 1. main에서 hotfix 브랜치 생성
git checkout main
git pull origin main
git checkout -b hotfix/cnv-scoring-fix

# 2. evidence_cnv/main.py 버그 수정

# 3. changepacks 실행 → evidence-cnv 선택 → Patch → 노트 작성
changepacks

# 4. 커밋 & push
git add -A
git commit -m "hotfix: CNV scoring 계산 오류 수정"
git push -u origin hotfix/cnv-scoring-fix

# 5. GitHub에서 main으로 PR 생성 → merge
#    ※ 핫픽스 PR의 changepacks check는 main 대상이므로
#      pr-changepacks-check.yaml (dev 대상)과 별도로 동작

# 6. CI가 자동으로:
#    - evidence v1.1.1 (Patch bump)
#    - version.py 갱신
#    - 태그 생성
#    - main → dev 역머지
```

**확인 포인트:**
- Patch 버전만 올라가는지 (v1.1.0 → v1.1.1)
- main → dev 역머지가 정상 동작하는지

---

## 로컬에서 수동 버전 업데이트 테스트

CI 없이 로컬에서 changepacks 동작을 직접 확인할 수 있습니다.

```bash
# 현재 프로젝트 상태 확인
changepacks check --tree

# 변경 로그 생성 (인터랙티브)
changepacks

# 버전 업데이트 미리보기
changepacks update --dry-run

# 버전 업데이트 적용
changepacks update --yes

# version.py 동기화
python scripts/sync_version.py

# 결과 확인
cat version.py
python evidence_snv/main.py
python pipeline/main.py
```

---

## 관련 문서

- [versioning_tool_first_docs.md](versioning_tool_first_docs.md) - 버저닝 툴 도입 배경 및 비교
- [jira_issue.md](jira_issue.md) - Jira + GitHub + Changepacks 연계 전체 가이드
