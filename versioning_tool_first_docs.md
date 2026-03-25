
배경

과거: vesion.py에 있는 숫자를 작업자가 main과 비교하여 major/minor.patch를 수정해야함. 아래과 같은 케이스에서 PR 순서가 꼬일 경우 버전 관리가 다운그레이드 될 수 있음. 

PR1, PR2 순으로 만들어짐. 

PR1 에서는 v5.3.2 로 버전 업, PR2 에서는 v5.4.0 으로 올라가는 상황

PR2 가 먼저 머지, PR1 이 나중에 머지될 때, PR1 작업자가 PR2 의 버전 업그레이드 정보를 놓친다면 v5.4.0 으로 업그레이드 됐다가 v5.3.2 로 다운그레이드 되는 상황

현재: Git Action CI으로 main 브랜치의 version.py을 읽어서 작업자에게 Git Action 메세지를 날리는 작업 완료. 그러나 알림의 기능일 뿐이지 작업자가 직접 작업 내용에 따라 버전을 수동으로 올려야함. 



SW팀 버저닝 툴

SW 팀은 JS 기반 버저닝 툴 changesets를 사용. Dev와 Main 브랜치가 분리되어있고 언어도 달라 EVIDENCE에도 직접 적용은 어렵지만, 플로우는 아래와 같음. 

개별 작업자가 개인 개발 브랜치에서 작업

Dev 브랜치에 개발 브랜치 머지할 때 “changesets” 명령어를 사용, changesets의 기능은 아래와 같음.

작업자는 작업이 major,minor,patch 중 어떤 것인지 노트와 함께 기재. 

changesets는 작업 디렉토리 /.changesets/some_work_hash.json을 만듦.

이 때, 작업자는 “본인” 작업에 대한 스케일만 고려함. 

여러 작업자들이 json 파일을 Dev에 쌓아놓고, Main에 Dev를 머지함.

CI에서 쌓여있는 json을 읽고 버전을 자동으로 업데이트함. 

이 때, 쌓여있는 버전 중 가장 스케일이 큰 버전으로 통일

Major 1개, Minor 3개, Patch 4개 (현재 1.0.0)

v.2.0.0으로 자동 업데이트 PR을 CI가 진행

위의 버전 자동관리 기능 이외에도 패키지 (디렉토리)별 버전 관리가 가능하다. 

EVIDENCE 적용

changesets를 직접 적용이 가능하긴 하나, CI용으로 Node.js나 npm을 깔아야함. 

Python에서 사용할 수 있는 프로그램은 아래와 같음. 

changepacks: Rust 기반 언어 중립적인 버전 관리 툴, changesets과 유사한 기능 제공

Python Semantic Release: Python 기반 버전 관리 툴, 파일 기반 버전 트래킹 하지 않으나, 커밋 메세지 기반 버전트래킹을 하므로, 커밋 메세지의 통일 필요. 

구분

Changepacks 

Python Semantic Release (PSR)

버전 판단 주체

사람 (명령어로 직접 선택)

기계 (커밋 메시지 분석)

기준 데이터

.changepacks/*.json 파일

Conventional Commits (커밋 문구)

자율성

리뷰 단계에서 유연하게 결정 가능

규칙(feat:, fix:)을 안 지키면 꼬임

난이도

낮음 (배우기 쉬움)

높음 (팀 전체가 커밋 규칙을 강제해야 함)

PR 커멘트를 받거나 black 적용같은 사소한 commit에도 매번 커밋 메세지 문구를 지켜야하고, 팀내 공유가 필요하기 때문에 Changepacks으로 개인 레파지토리에서 테스트함. 

워크플로우

1. 개인 로컬 작업 (개발 단계)

평소처럼 자유롭게 add, commit을 반복하며 기능을 구현합니다.

이때 반드시 changepacks를 실행할 필요는 없습니다. (리뷰 과정에서 코드가 크게 바뀔 수 있으니까요.)

2. PR 생성 및 리뷰 대응 (확정 단계)

리뷰가 완료되고 "이제 머지해도 되겠다" 싶은 시점에 로컬에서 changepacks를 실행합니다.

이때 Major / Minor / Patch 중 하나를 선택하여 "예약 파일(JSON)"을 생성합니다.

생성된 JSON 파일을 커밋에 포함하여 Push합니다.

3. 메인 머지 및 자동 버저닝 (CI 단계)

PR이 main 브랜치에 머지되면 GitHub Actions가 자동으로 구동됩니다.

CI는 쌓여있는 JSON 파일을 읽어 version.py와 pyproject.toml(CI 설정 파일)의 숫자를 실제로 업데이트합니다.

숫자가 바뀐 코드를 main에 자동 커밋하고 Git Tag를 생성합니다.

4. 여러 작업이 누적된 경우(JSON 파일이 여러 개) 어떻게 되나요?

한 PR에 JSON 파일이 2개 이상 포함되어 머지되면, changepacks는 이를 **합산(Combine)**합니다.

예시: * 첫 커밋에서 patch 로그 생성

리뷰 수정 후 추가로 patch 로그 생성

결과: 머지 시 CI는 "Patch + Patch"로 인식하여 버전을 두 단계 올리는 게 아니라, 해당 패키지에 대해 가장 높은 등급 하나만 적용하거나 누적된 변경사항으로 취급합니다. (보통은 동일 패키지에 대해 하나로 병합하여 처리합니다.)

리뷰 수정 후 추가로 minor 로그 생성

결과: 머지 시 CI는 "Patch + Minor"로 인식하여 해당 패키지에 대해 가장 높은 등급(Minor) 하나만 적용하거나 누적된 변경사항으로 취급합니다.

개인 로컬 레파지토리에서 테스트 해 봄. 꽤 세팅할게 많음… changepacks 명령어를 치면 프로젝트를 선택하고 (테스트는 1개만 있음) 버전을 선택함. 자동으로 json이 만들어짐. 



결론:

"버전 숫자를 직접 고치지 마세요": version.py는 CI가 고칠 영역입니다. 사람은 changepacks 명령어만 쓰면 됩니다.

"로그 파일은 예약권입니다": 이 JSON 파일이 PR에 포함되지 않으면 머지해도 버전이 올라가지 않습니다. (무조건 add / commit 해야함.)

“충돌 걱정 제로": 각자 다른 이름의 JSON 파일로 예약하기 때문에, 여러 명이 동시에 머지해도 version.py 파일 충돌(Conflict)이 발생하지 않습니다.

고려해볼만한 점

EVIDENCE.tucuxi는 dev 브랜치가 없기 때문에 현행 방법으로도 버전이 꼬이지 않는 버전관리는 어느 정도 가능

dev 브랜치로 분리되면 버전관리 툴이 지금보다 더 필요함. 

패키지(디렉토리)별 버전관리가 가능하다.

현행은 evidence* 파일들을 뭉뚱그려 EVIDENCE.tucuxi의 버전으로 다루고 있음. 

pipeline / reanalysis 버전에 대한 개별 관리가 가능하다. (개별 디렉토리에 pyproject.toml을 넣으면 됨)

과거 머지된 브랜치에서 이어서 작업할 경우 Json 파일들을 지워주긴 해야함. 

GitHub에서는 한 번 버전 올리며 머지할 경우 version 관련 json 파일들을 지움. 

개인 로컬에서 다른 작업을 하다 json 을 같이 push 하면 의도치 않은 버전이 올라갈 수 있음. 

지금 만들어둔 알림 기능을 changepacks를 쓴다고 하더라도, json 파일을 추적해 알림 발송 기능은 만들어두어야하지 않나?라는 의견
