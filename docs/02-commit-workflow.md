# 변경을 검토 가능한 커밋으로 만들기

## 목표

수정한 파일을 전부 한 번에 커밋하는 것이 아니라 **변경 목적을 기준으로 커밋을 구성하고, 실제 커밋에 들어갈 diff를 확인한 뒤 검증을 통과시킵니다.**

기본 흐름은 다음과 같습니다.

```text
현재 변경 확인
→ 변경 목적 구분
→ 필요한 변경만 스테이징
→ 스테이징된 diff 검토
→ 프로젝트 검사
→ 커밋
→ 생성된 커밋과 남은 변경 재확인
```

핵심은 다음입니다.

```text
"수정한 파일"을 커밋하는 것이 아니라
"하나의 목적을 가진 변경"을 커밋한다.
```

---

## 세 상태를 다시 확인하기

Git의 변경 검토는 다음 세 상태 사이의 비교입니다.

```text
작업 트리     현재 디스크에 존재하는 파일 내용
인덱스        다음 커밋에 포함할 것으로 선택한 상태
HEAD          현재 브랜치의 마지막 커밋
```

각 diff 명령은 비교 대상이 다릅니다.

```bash
git diff
```

```text
작업 트리 ↔ 인덱스
```

즉, **아직 스테이징하지 않은 변경**을 보여 줍니다.

```bash
git diff --staged
```

```text
인덱스 ↔ HEAD
```

즉, **다음 커밋에 실제로 들어갈 변경**을 보여 줍니다.

`--cached`도 같은 의미로 사용할 수 있습니다.

```bash
git diff --cached
```

마지막으로:

```bash
git diff HEAD
```

은 현재 작업 트리를 `HEAD`와 비교합니다.

개념적으로:

```text
HEAD
 ├─ staged 변경
 └─ unstaged 변경

전체 결과를 작업 트리와 비교
```

따라서 현재 로컬에 존재하는 전체 수정 범위를 확인할 때 유용합니다.

---

## `git diff`가 비어 있어도 변경이 없다는 뜻은 아니다

예를 들어:

```bash
git add README.md
```

를 실행했다면 작업 트리와 인덱스의 `README.md` 내용은 같아집니다.

이때:

```bash
git diff
```

가 비어 있을 수 있습니다.

하지만:

```bash
git diff --staged
```

에는 변경이 남아 있습니다.

즉:

```text
git diff가 비어 있음
≠
커밋할 변경이 없음
```

다음 커밋의 내용은 반드시:

```bash
git diff --staged
```

로 확인합니다.

---

# `git status --short` 읽기

축약 출력은 일반적으로 파일명 앞의 두 칸으로 상태를 표현합니다.

```text
XY path
```

개념적으로:

```text
X = 인덱스 상태
Y = 작업 트리 상태
```

예:

```text
M  src/app.py
 M README.md
MM config.yml
?? notes.txt
```

의미는 다음과 같습니다.

```text
M  src/app.py
↑
인덱스에 수정된 내용이 있음
작업 트리는 그 이후 추가 수정 없음
```

```text
 M README.md
 ↑
 작업 트리에만 수정이 있음
 아직 스테이징하지 않음
```

```text
MM config.yml
↑↑
│└ 작업 트리에도 추가 수정이 있음
└  인덱스에도 수정이 있음
```

`MM`은 특히 중요합니다.

예를 들어:

```text
HEAD 버전
   ↓
파일 수정 A
   ↓
git add
   ↓
인덱스 = 수정 A
   ↓
파일 추가 수정 B
```

가 되면:

```text
HEAD          원본
인덱스        수정 A
작업 트리     수정 A + 수정 B
```

이므로 `MM`으로 표시될 수 있습니다.

이 상태에서 커밋하면 **수정 A만 들어가고 수정 B는 남습니다.**

---

## 미추적 파일

```text
?? notes.txt
```

는 아직 Git이 추적하지 않는 파일입니다.

일반적인:

```bash
git diff
```

는 미추적 파일 전체 내용을 diff로 보여 주지 않습니다.

따라서:

```bash
git status --short
```

에서 발견한 뒤 직접 파일을 확인해야 합니다.

예:

```bash
sed -n '1,160p' notes.txt
```

또는 적절한 편집기나 파일 조회 명령을 사용합니다.

---

# 파일 수가 아니라 변경 목적을 정하기

한 작업 중 다음 변경이 생겼다고 가정합니다.

```text
A. 제목 검증 규칙 변경
B. 새 규칙을 검증하는 테스트 추가
C. README의 제목 규칙 설명 수정
D. README에서 발견한 무관한 오탈자 수정
E. 개인 디버그 메모 생성
```

파일 기준으로 보면 README 변경이 하나처럼 보일 수 있습니다.

하지만 목적 기준으로 보면 다릅니다.

```text
커밋 1
- 제목 검증 규칙 변경
- 관련 테스트
- 관련 README 설명

커밋 2
- 무관한 README 오탈자 수정

커밋하지 않음
- 개인 디버그 메모
```

좋은 기준은 다음과 같습니다.

> 이 커밋만 독립적으로 리뷰하거나 되돌렸을 때 하나의 명확한 의도가 유지되는가?

예를 들어 검증 코드는 바뀌었는데 테스트가 다음 커밋에 있다면 첫 커밋만 checkout했을 때 프로젝트 검증이 깨질 수 있습니다.

반대로 기능 변경과 아무 관계없는 오탈자를 굳이 같은 커밋에 넣을 이유도 없습니다.

---

# 스테이징하기 전 diff 읽기

먼저 전체 상황을 확인합니다.

```bash
git status --short
git diff --stat
git diff
```

각 명령의 역할:

```text
git status --short
→ 어떤 파일이 어떤 상태인가?

git diff --stat
→ 변경 규모가 어느 정도인가?

git diff
→ 아직 스테이징하지 않은 실제 변경 내용은 무엇인가?
```

확인할 내용:

* 예상한 파일만 수정되었는가?
* 예상하지 못한 파일 삭제가 있는가?
* 실행 권한이 바뀐 파일이 있는가?
* 생성 파일이 들어왔는가?
* IDE나 운영체제 개인 설정 파일이 포함되었는가?
* 로그나 디버그 출력이 남아 있는가?
* 비밀값이 추가되었는가?
* 테스트 변경이 실제 동작 변경과 일치하는가?
* 문서 설명이 실제 구현과 일치하는가?

---

# 파일 전체가 같은 목적이면 경로를 명시해 스테이징

예:

```bash
git add src/validator.py tests/test_validator.py
```

이는 해당 경로의 현재 변경을 인덱스에 반영합니다.

그 뒤 반드시 확인합니다.

```bash
git diff --staged
```

`git add`는 커밋이 아닙니다.

잘못 스테이징했다면 아직 수정할 수 있습니다.

---

# 같은 파일에 여러 목적이 섞였으면 부분 스테이징

예를 들어 `README.md` 안에:

```text
제목 검증 설명 수정
+
무관한 오탈자 수정
```

이 함께 있다면 파일 전체를 스테이징할 필요가 없습니다.

```bash
git add -p README.md
```

Git이 변경을 hunk 단위로 보여 주며 스테이징 여부를 묻습니다.

자주 사용하는 입력:

```text
y  현재 hunk를 스테이징
n  현재 hunk를 스테이징하지 않음
s  가능한 경우 더 작은 hunk로 분리
q  종료
?  도움말
```

예:

```text
Stage this hunk [y,n,q,a,d,s,e,?]?
```

여기서 `s`는 Git이 현재 hunk를 더 작은 독립 변경으로 분리할 수 있을 때 유용합니다.

---

## hunk는 변경 목적과 항상 일치하지 않는다

Git의 hunk는 **의미 단위가 아니라 diff 문맥을 기준으로 만들어진 변경 조각**입니다.

따라서 논리적으로 서로 다른 두 변경이 가까운 줄에 있으면 하나의 hunk로 묶일 수 있습니다.

반대로 하나의 기능 변경이 여러 hunk로 나뉠 수도 있습니다.

즉:

```text
hunk = 커밋 단위
```

가 아닙니다.

`git add -p`의 목적은 Git이 자동으로 커밋 구조를 결정하게 하는 것이 아니라, **개발자가 의도한 변경만 인덱스에 선택적으로 올리는 것**입니다.

---

# `git add .`는 금지 명령이 아니다

다음 명령 자체가 잘못된 것은 아닙니다.

```bash
git add .
```

문제는 **무엇이 포함될지 확인하지 않은 채 사용하는 것**입니다.

예를 들어 현재 작업 트리에:

```text
src/app.py
tests/test_app.py
.env
notes/debug.txt
build/output.bin
```

이 함께 있다면 무심코 모두 스테이징할 수 있습니다.

반대로 이미:

```bash
git status --short
git diff
```

를 확인했고 모든 변경이 하나의 커밋에 정확히 들어가야 한다면 `git add .`도 합리적일 수 있습니다.

도구보다 중요한 것은 포함 범위를 알고 있는지입니다.

---

# 잘못 스테이징했을 때

파일 수정은 유지하면서 인덱스에서만 제거하려면:

```bash
git restore --staged path/to/file
```

예:

```bash
git restore --staged README.md
```

상태 변화:

```text
실행 전

HEAD          원본
인덱스        수정본
작업 트리     수정본
```

```text
실행 후

HEAD          원본
인덱스        HEAD와 같은 상태
작업 트리     수정본
```

즉, 파일 수정은 사라지지 않습니다.

전체 스테이징을 다시 선택하려면:

```bash
git restore --staged .
```

---

## `git restore`와 `git restore --staged`는 다르다

다음 명령은 의미가 크게 다릅니다.

```bash
git restore --staged README.md
```

```text
인덱스에서만 변경 제거
작업 트리 수정은 유지
```

반면:

```bash
git restore README.md
```

는 기본적으로 작업 트리 파일을 인덱스 상태로 복원합니다.

즉, 아직 다른 곳에 보존하지 않은 작업 트리 수정이 사라질 수 있습니다.

따라서 복구 목적이라면 항상 먼저 질문합니다.

```text
버리려는 대상이 인덱스 상태인가?
작업 트리의 실제 수정 내용인가?
```

---

# 커밋 직전 확인

최소한 다음을 확인합니다.

```bash
git status --short
git diff --staged --check
git diff --staged
```

`git diff --staged --check`는 일반적인 내용 검토를 대신하지 않습니다.

주로 다음과 같은 공백 오류를 탐지합니다.

* 줄 끝의 불필요한 공백
* 일부 잘못된 공백 패턴

따라서:

```bash
git diff --staged --check
```

가 성공했다고 해서 코드가 올바르거나 커밋 내용이 적절하다는 뜻은 아닙니다.

실제 변경 내용은 여전히:

```bash
git diff --staged
```

로 읽어야 합니다.

---

## 커밋 전 점검

```text
[ ] 하나의 명확한 변경 목적만 포함했는가?
[ ] 기능 변경과 이를 검증하는 테스트가 적절히 함께 있는가?
[ ] 관련 없는 정리나 포맷 변경이 섞이지 않았는가?
[ ] 실제 동작과 문서 설명이 일치하는가?
[ ] 비밀값이 포함되지 않았는가?
[ ] 개인 메모가 포함되지 않았는가?
[ ] 빌드 결과물이나 생성 파일이 실수로 포함되지 않았는가?
[ ] 예상하지 못한 파일 삭제가 없는가?
[ ] 예상하지 못한 실행 권한 변경이 없는가?
[ ] 디버그 코드와 임시 출력이 남아 있지 않은가?
```

---

# 프로젝트 검사와 커밋

저장소가 지정한 검사를 실행합니다.

예:

```bash
./scripts/check.sh
```

프로젝트에 따라 실제 명령은 다를 수 있습니다.

예:

```text
unit test
integration test
lint
type check
format check
build
static analysis
```

저장소의 `README`, `CONTRIBUTING`, CI 설정에 정의된 검사를 우선합니다.

검사가 성공한 뒤 커밋합니다.

```bash
git commit -m "feat: validate change record title"
```

---

# 커밋 제목

Git 자체는 다음 형식을 요구하지 않습니다.

```text
feat:
fix:
docs:
refactor:
```

이는 Conventional Commits 같은 별도 규칙입니다.

저장소가 해당 규칙을 사용한다면 따릅니다.

예:

```text
feat: validate change record title
fix: reject empty change title
docs: clarify title length requirement
test: cover title boundary cases
```

별도 규칙이 없다면 적어도 **무엇이 바뀌었는지 식별 가능한 제목**을 사용합니다.

피할 제목:

```text
update files
fix stuff
changes
work in progress
final
misc
```

이런 제목은 나중에:

```bash
git log
git bisect
git blame
git revert
```

등으로 이력을 추적할 때 거의 정보를 주지 못합니다.

---

# 커밋 결과 확인

커밋 직후 확인합니다.

```bash
git show --stat --oneline HEAD
git show --format=fuller --no-ext-diff HEAD
git status --short
```

첫 명령:

```bash
git show --stat --oneline HEAD
```

은 커밋 제목과 변경 파일 규모를 빠르게 보여 줍니다.

두 번째:

```bash
git show --format=fuller --no-ext-diff HEAD
```

은 작성자와 커미터 정보, 커밋 내용 등을 더 자세히 확인할 수 있습니다.

필요하다면 실제 patch까지 확인합니다.

```bash
git show HEAD
```

그리고:

```bash
git status --short
```

로 커밋하지 않은 변경이 무엇인지 다시 확인합니다.

---

# 관련 없는 변경은 별도 커밋으로 분리

첫 번째 커밋을 만든 뒤 남은 변경을 다시 읽습니다.

```bash
git status --short
git diff
```

예를 들어 첫 커밋에서 기능 변경을 처리한 뒤 README 오탈자만 남았다면:

```bash
git add README.md
git diff --staged --check
git diff --staged
git commit -m "docs: fix dependency spelling"
```

처럼 별도 커밋으로 만들 수 있습니다.

핵심은 커밋 개수 자체를 최소화하는 것이 아닙니다.

```text
너무 큰 커밋
→ 서로 다른 이유의 변경이 섞임

너무 작은 커밋
→ 하나의 기능이 무의미하게 잘게 분리됨
→ 중간 커밋에서 빌드나 테스트가 깨질 수 있음
```

좋은 기준은:

> 각 커밋이 하나의 개발 의도를 가지면서 가능한 한 독립적으로 검토·검증·되돌리기 쉬운가?

입니다.

---

# `.gitignore`와 `.git/info/exclude`

무시 규칙은 **누구에게 적용되어야 하는지**에 따라 위치를 선택합니다.

---

## 모든 복제본에서 무시해야 하는 파일

프로젝트 공통 규칙이라면 `.gitignore`에 기록하고 커밋합니다.

예:

```gitignore
build/
__pycache__/
.env.local
```

이 규칙은 저장소 이력에 포함되므로 다른 개발자와 CI 환경에도 공유됩니다.

적합한 예:

```text
빌드 결과물
언어 런타임 캐시
프로젝트 공통 로컬 환경 파일
IDE 프로젝트에서 공통적으로 생성되는 불필요 파일
```

단, 실제로 어떤 파일을 무시해야 하는지는 프로젝트 정책에 따라 달라집니다.

---

## 현재 복제본에서만 무시할 파일

개인 메모처럼 다른 사람에게 공유할 필요가 없는 규칙은:

```text
.git/info/exclude
```

에 둘 수 있습니다.

예:

```bash
printf '%s\n' 'notes/' >> .git/info/exclude
```

이 규칙은 현재 로컬 저장소에만 적용되며 일반적인 Git push로 공유되지 않습니다.

적합한 예:

```text
개인 디버그 메모
개인 실험 파일
현재 복제본에서만 사용하는 임시 디렉터리
```

---

## 이미 추적 중인 파일에는 ignore 규칙이 소급 적용되지 않는다

예를 들어 이미 Git에 커밋된:

```text
config/local.env
```

파일을 나중에 `.gitignore`에 추가해도 Git은 해당 파일을 계속 추적합니다.

`.gitignore`는 기본적으로 **아직 추적하지 않는 파일을 새로 추적하지 않도록 하는 규칙**입니다.

팀이 정말로 추적을 중단하기로 했다면 별도의 변경으로 처리해야 합니다.

예를 들어 상황에 따라:

```bash
git rm --cached path/to/file
```

을 사용할 수 있지만, 이는 저장소의 추적 상태를 변경하므로 팀 정책과 목적을 확인한 뒤 실행해야 합니다.

---

# 마지막 로컬 커밋 수정하기

아직 공유하지 않은 마지막 커밋에 작은 누락이 있다면 `amend`를 사용할 수 있습니다.

```bash
# 누락된 수정
git add path/to/file
git diff --staged
git commit --amend --no-edit
```

여기서 중요한 점은 `amend`가 기존 커밋 객체를 내부에서 수정하는 기능이 아니라는 것입니다.

개념적으로:

```text
기존 커밋 C
```

를 수정하는 것이 아니라:

```text
새 커밋 C'
```

를 만들고 현재 브랜치가 C'를 가리키게 합니다.

따라서 커밋 해시가 바뀝니다.

```text
기존

A → B → C
        ↑
       HEAD
```

```text
amend 후

A → B → C'
        ↑
       HEAD

C는 현재 브랜치 이력에서 벗어남
```

---

## 공유한 커밋을 amend할 때의 문제

이미 원격에 push한 C를 로컬에서 C'로 amend하면:

```text
원격     A → B → C

로컬     A → B → C'
```

처럼 서로 다른 이력이 됩니다.

일반 push는 거부될 수 있으며, 원격 브랜치를 C'로 바꾸려면 이력 재작성이 필요합니다.

이 경우 보통 force push 계열이 필요하므로 팀 정책을 먼저 확인해야 합니다.

공유 브랜치에서는 특히 주의합니다.

---

# `local-git-lab`에서 연습하기

먼저 실습 상태를 새로 만듭니다.

기존 상태를 버려도 되는지 확인한 뒤:

```bash
cd exercises/local-git-lab
./git-lab.sh --reset sample
cd lab/sample-app
```

작업 브랜치를 만듭니다.

```bash
git switch --no-track -c feature/document-title origin/main
```

확인:

```bash
git status --short --branch
git branch -vv
```

---

## 서로 다른 목적의 변경 만들기

첫 번째 변경은 제목 규칙 설명이고, 두 번째 변경은 의존성 문장 보완입니다.

```bash
python3 - <<'PY'
from pathlib import Path

path = Path("README.md")
text = path.read_text(encoding="utf-8")

text = text.replace(
    "이 저장소에는 3자 이상 60자 이하의 작업 제목만 허용하는\n"
    "POSIX 셸 검증 도구가 포함되어 있습니다.",
    "작업 제목은 3자 이상 60자 이하여야 합니다.\n"
    "POSIX 셸 스크립트가 이 규칙을 검사합니다.",
)

text = text.replace(
    "외부 패키지는 필요하지 않습니다.",
    "실행 시 외부 패키지는 필요하지 않습니다.",
)

path.write_text(text, encoding="utf-8")
PY
```

개인 파일도 만듭니다.

```bash
mkdir -p notes
printf '개인 메모\n' > notes/debug.txt
```

이제:

```bash
git status --short
```

에서 대략 다음 종류의 상태를 볼 수 있습니다.

```text
 M README.md
?? notes/
```

---

## 첫 번째 목적만 스테이징

```bash
git add -p README.md
```

제목 규칙 설명에 해당하는 hunk만 선택합니다.

그 뒤:

```bash
git diff --staged
```

에서 첫 번째 목적만 들어갔는지 확인합니다.

동시에:

```bash
git diff
```

에서는 두 번째 README 수정이 남아 있어야 합니다.

`notes/debug.txt`는 미추적 파일이므로 커밋에 넣지 않습니다.

---

## 검사 후 첫 번째 커밋

```bash
git diff --staged --check
./scripts/test.sh
```

성공하면 커밋합니다.

예:

```bash
git commit -m "docs: clarify title validation rule"
```

그 뒤:

```bash
git status --short
git diff
```

를 확인합니다.

첫 번째 목적은 커밋되었고:

```text
의존성 문장 수정
개인 notes 파일
```

만 남아 있어야 합니다.

---

## 두 번째 목적 커밋

남은 README 변경을 확인합니다.

```bash
git diff README.md
```

스테이징합니다.

```bash
git add README.md
git diff --staged --check
git diff --staged
```

검사:

```bash
./scripts/test.sh
```

커밋:

```bash
git commit -m "docs: clarify runtime dependency"
```

---

## 결과 확인

```bash
git log --oneline origin/main..HEAD
git status --short
```

의도한 결과는 개념적으로 다음과 같습니다.

```text
커밋 2  의존성 문장 보완
커밋 1  제목 규칙 설명
origin/main
```

그리고 개인 메모는 여전히 커밋되지 않은 상태로 남습니다.

```text
?? notes/
```

필요하다면 현재 복제본에서만 무시합니다.

```bash
printf '%s\n' 'notes/' >> .git/info/exclude
```

확인:

```bash
git status --short
```

---

## 두 README 변경이 하나의 hunk로 잡히는 경우

`git add -p README.md`에서 `s`를 눌러도 나뉘지 않을 수 있습니다.

이는 두 변경이 diff상 너무 가까이 있기 때문입니다.

이 경우 중요한 것은 `git add -p` 자체를 반드시 성공시키는 것이 아닙니다.

목표는:

```text
첫 커밋에는 첫 번째 목적만
두 번째 커밋에는 두 번째 목적만
```

이 들어가도록 만드는 것입니다.

필요하다면:

* 파일을 일시적으로 편집해 한 변경만 남긴 뒤 스테이징
* 스테이징 후 두 번째 변경을 다시 적용
* `git add -p`의 더 세밀한 편집 기능 사용

등의 방법을 사용할 수 있습니다.

즉, 도구 사용법보다 **최종 인덱스의 내용**이 중요합니다.
