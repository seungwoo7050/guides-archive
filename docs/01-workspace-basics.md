# 작업을 시작하기 전 Git 상태 확인

## 목표

코드를 수정하기 전에 **현재 저장소가 무엇인지, 어떤 커밋을 기준으로 작업하는지, 로컬에 남아 있는 변경이 무엇인지** 먼저 확인합니다.

이 문서를 마치면 다음 질문에 명령으로 답할 수 있어야 합니다.

* 지금 어느 저장소에 있습니까?
* 새 커밋에 기록될 작성자 이름과 이메일은 무엇입니까?
* 어느 원격 저장소와 연결되어 있습니까?
* 현재 브랜치와 upstream은 무엇입니까?
* 로컬의 `origin/main` 정보는 최신입니까?
* 작업 트리나 인덱스에 이전 작업이 남아 있습니까?
* 새 작업 브랜치는 정확히 어느 커밋에서 시작합니까?

---

## 먼저 구분할 상태

Git을 사용할 때 가장 먼저 구분해야 하는 것은 **작업 트리**, **인덱스**, **`HEAD`**입니다.

```text
작업 트리     현재 디렉터리에 실제로 존재하는 파일 내용
인덱스        다음 커밋에 포함하기 위해 선택해 둔 상태
HEAD          현재 체크아웃한 커밋을 가리키는 참조
```

보통 브랜치를 체크아웃한 상태에서는 `HEAD`가 브랜치를 가리키고, 그 브랜치가 다시 커밋을 가리킵니다.

```text
HEAD
  ↓
feature/title-check
  ↓
커밋 C
```

파일을 수정했다고 해서 세 상태가 모두 동시에 바뀌는 것은 아닙니다.

```text
파일 수정
→ 작업 트리만 변경

git add
→ 선택한 변경이 인덱스에 반영

git commit
→ 인덱스 상태로 새 커밋 생성
→ 현재 브랜치가 새 커밋으로 이동
```

예를 들어 `README.md`를 수정했지만 아직 `git add`를 하지 않았다면:

```text
HEAD의 README.md       이전 내용
인덱스의 README.md     이전 내용
작업 트리의 README.md  수정한 내용
```

`git add README.md`를 실행하면:

```text
HEAD의 README.md       이전 내용
인덱스의 README.md     수정한 내용
작업 트리의 README.md  수정한 내용
```

이 구분을 이해해야 `git diff`, `git diff --staged`, `git restore` 같은 명령을 안전하게 사용할 수 있습니다.

---

## 로컬 브랜치와 원격 추적 브랜치

다음 두 이름은 같은 것이 아닙니다.

```text
main
origin/main
```

`main`은 **현재 컴퓨터에 존재하는 로컬 브랜치**입니다.

`origin/main`은 **마지막으로 원격 상태를 확인했을 때의 `origin` 저장소의 `main` 위치를 로컬에 기록해 둔 원격 추적 브랜치(remote-tracking branch)**입니다.

```text
원격 저장소의 main
        │
        │ git fetch
        ▼
로컬의 origin/main
```

따라서 `origin/main`은 원격 서버를 실시간으로 읽는 이름이 아닙니다.

다른 사람이 GitHub의 `main`에 새 커밋을 push해도 내가 아직 `fetch`하지 않았다면:

```text
GitHub main       → 새 커밋 D
origin/main       → 이전 커밋 C
```

일 수 있습니다.

이 때문에 **`origin/main`을 작업 기준점으로 사용하기 전에 먼저 `fetch`해야 합니다.**

---

## `HEAD`가 의미하는 것

`HEAD`는 현재 작업 위치를 나타냅니다.

일반적인 브랜치 작업 상태는 다음과 같습니다.

```text
HEAD → feature/title-check → 커밋 C
```

새 커밋을 만들면:

```text
git commit
```

새 커밋 D가 생성되고 브랜치가 이동합니다.

```text
HEAD → feature/title-check → 커밋 D
                           ↘
                            커밋 C
```

즉, 보통 `HEAD` 자체를 직접 앞으로 이동시키는 것이 아니라 **`HEAD`가 가리키는 현재 브랜치가 새 커밋으로 이동합니다.**

단, 특정 커밋을 직접 checkout하거나 switch하면 `HEAD`가 브랜치가 아닌 커밋을 직접 가리키는 **detached HEAD** 상태가 될 수도 있습니다.

현재 일반 브랜치 작업 상태인지 확인하려면:

```bash
git branch --show-current
```

을 사용할 수 있습니다.

---

## 작성자 정보와 원격 인증 계정

Git의 **커밋 작성자 정보**와 **원격 저장소 인증 정보**는 별개입니다.

```text
user.name
user.email
→ 커밋 객체에 기록되는 이름과 이메일

HTTPS credential
SSH 키
SSO 인증
→ GitHub/GitLab 등의 원격 저장소 접근 권한을 증명
```

예를 들어 GitHub에 정상적으로 push할 수 있어도:

```bash
git config user.email
```

이 개인 이메일로 잘못 설정되어 있을 수 있습니다.

반대로 올바른 회사 이메일이 설정되어 있다고 해서 그 계정으로 원격 저장소에 접근할 수 있다는 뜻도 아닙니다.

따라서 둘을 각각 확인해야 합니다.

---

# 팀에서 먼저 확인할 사항

다음 항목은 Git 자체의 기능이 아니라 **저장소 운영 정책**입니다.

* 저장소 URL
* 기본 브랜치 이름
* 조직 저장소에 직접 push하는지, fork를 사용하는지
* 브랜치 이름 규칙
* 회사 이메일 또는 noreply 이메일 사용 여부
* HTTPS, SSH, SSO 중 사용할 인증 방식
* 작업 브랜치에서 강제 push가 허용되는지
* Pull Request에 필요한 리뷰 수
* 필수 CI 검사
* 보호 브랜치 규칙

모르면 추측하지 않습니다.

먼저 다음 문서를 확인합니다.

```text
README
CONTRIBUTING
DEVELOPMENT
팀 개발 문서
저장소의 branch protection 규칙
```

Git 명령이 기술적으로 가능하다는 것과 팀에서 허용된다는 것은 별개의 문제입니다.

---

# 현재 저장소 확인

다음 명령들은 일반적으로 저장소 파일이나 커밋을 변경하지 않는 조회 명령입니다.

```bash
git rev-parse --show-toplevel
git status --short --branch
git branch --show-current
git branch -vv
git remote -v
git log -1 --oneline --decorate
```

각 명령은 서로 다른 질문에 답합니다.

```text
git rev-parse --show-toplevel
→ 저장소 루트는 어디인가?

git status --short --branch
→ 현재 브랜치와 작업 트리 상태는 어떤가?

git branch --show-current
→ 현재 브랜치 이름은 무엇인가?

git branch -vv
→ 각 로컬 브랜치의 최신 커밋과 upstream은 무엇인가?

git remote -v
→ 어느 원격 저장소에서 fetch하고 어디로 push하는가?

git log -1 --oneline --decorate
→ 현재 HEAD는 어느 커밋인가?
```

---

## 저장소 루트

```bash
git rev-parse --show-toplevel
```

예:

```text
/home/seungwoo/projects/sample-app
```

현재 셸의 디렉터리 이름만 보고 저장소를 판단하지 않습니다.

특히 다음 상황에서는 확인이 중요합니다.

```text
sample-app/
sample-app-old/
sample-app-test/
sample-app-worktree/
```

여러 복제본이나 Git worktree를 동시에 사용하면 터미널을 잘못 열어 다른 저장소를 수정하는 일이 생길 수 있습니다.

출력된 절대 경로가 실제로 작업하려던 저장소인지 확인합니다.

---

## 작성자 정보

현재 커밋에 사용될 작성자 설정을 확인합니다.

```bash
git config --show-origin --get user.name
git config --show-origin --get user.email
```

예:

```text
file:/home/user/.gitconfig Seungwoo Kim
file:.git/config name@example.com
```

`--show-origin`은 단순히 값만 보여 주는 것이 아니라 **그 값이 어느 설정 파일에서 왔는지**도 보여 줍니다.

Git 설정은 여러 범위에 존재할 수 있습니다.

```text
system
global
local
worktree
```

일반적으로 저장소의 local 설정은 global 설정보다 우선합니다.

회사와 개인 저장소를 한 컴퓨터에서 함께 사용한다면 저장소별 설정을 두는 것이 안전합니다.

```bash
git config --local user.name "Seungwoo Kim"
git config --local user.email "name@example.com"
```

확인:

```bash
git config --show-origin --get user.name
git config --show-origin --get user.email
```

---

## 원격 URL

```bash
git remote -v
```

예:

```text
origin  git@github.com:example/sample-app.git (fetch)
origin  git@github.com:example/sample-app.git (push)
```

확인할 항목:

* 저장소 소유자가 맞는가?
* 저장소 이름이 맞는가?
* 회사 Git 호스트인지 공개 GitHub인지 맞는가?
* fetch URL이 올바른가?
* push URL이 올바른가?
* HTTPS와 SSH 중 팀에서 정한 방식과 일치하는가?

Git은 fetch URL과 push URL을 서로 다르게 설정할 수도 있으므로 둘 다 확인합니다.

URL이 잘못되었다면 먼저 정확한 대상 URL을 확인한 뒤 수정합니다.

```bash
git remote set-url origin CORRECT_URL
```

변경 후 다시 확인합니다.

```bash
git remote -v
```

---

## 작업 트리와 브랜치

```bash
git status --short --branch
git branch -vv
```

변경이 없는 예:

```text
## main...origin/main
```

그리고:

```text
* main abc1234 [origin/main] chore: baseline
```

첫 출력은 현재 브랜치가 `main`이고 `origin/main`을 기준으로 비교하고 있음을 보여 줍니다.

두 번째 출력은:

```text
현재 브랜치: main
현재 커밋: abc1234
upstream: origin/main
```

임을 보여 줍니다.

변경이 있다면:

```text
## main...origin/main
 M config/app.yml
?? notes/debug.txt
```

여기서:

```text
 M config/app.yml
```

은 추적 중인 파일이 작업 트리에서 수정되었다는 뜻이고,

```text
?? notes/debug.txt
```

는 Git이 아직 추적하지 않는 파일이라는 뜻입니다.

예상하지 못한 변경을 발견했다고 해서 즉시 다음을 실행하면 안 됩니다.

```bash
git restore .
git clean -fd
git reset --hard
```

이 명령들은 실제 작업을 삭제할 수 있습니다.

먼저 확인합니다.

* 내가 만든 변경인가?
* 다른 터미널이나 도구가 만든 변경인가?
* 이전 작업의 미완성 상태인가?
* 보존해야 하는가?
* 별도 브랜치나 커밋으로 옮겨야 하는가?

---

# `origin/main`이 언제 갱신됐는지 확인하기

여기서 중요한 구분이 하나 있습니다.

Git은 일반적으로 **"`origin/main`을 마지막으로 fetch한 시각"을 ref 자체에 직접 기록하지 않습니다.**

따라서 다음 질문은 서로 다릅니다.

```text
origin/main이 가리키는 커밋은 언제 만들어졌는가?
마지막 fetch는 언제 실행했는가?
현재 원격 main이 origin/main보다 새롭지는 않은가?
```

첫 번째는 커밋 날짜를 확인할 수 있습니다.

```bash
git log -1 --format=fuller origin/main
```

하지만 이것은 **fetch 시각이 아니라 해당 커밋의 작성/커밋 시각**입니다.

현재 원격 상태와 동기화되었는지 확실히 확인하려면 가장 안전한 방법은 직접 fetch하는 것입니다.

```bash
git fetch origin
```

그 뒤 `origin/main`을 기준점으로 사용합니다.

---

# `fetch`가 바꾸는 것

실행 전에 무엇이 바뀌는지 알고 있어야 합니다.

```bash
git fetch origin
```

일반적인 효과는 다음과 같습니다.

* 원격 저장소에서 새 Git 객체를 내려받습니다.
* `origin/main`, `origin/develop` 같은 원격 추적 ref를 갱신합니다.
* 새 원격 브랜치 정보를 가져올 수 있습니다.
* 현재 로컬 브랜치를 자동으로 merge하지 않습니다.
* 현재 로컬 브랜치를 자동으로 rebase하지 않습니다.
* 작업 트리 파일을 원격 버전으로 자동 교체하지 않습니다.

예를 들어 fetch 전:

```text
main         A---B
                  \
origin/main        C

GitHub main        C---D---E
```

라면 fetch 후:

```text
main         A---B

origin/main  A---B---C---D---E
```

처럼 `origin/main`이 갱신될 수 있습니다.

현재 `main` 브랜치는 자동으로 E까지 이동하지 않습니다.

---

## fetch 전후 확인

```bash
git status --short --branch
git branch -vv

git fetch origin

git status --short --branch
git branch -vv
git log --oneline --decorate --graph --all -12
```

예를 들어 fetch 뒤:

```text
## main...origin/main [behind 2]
```

가 보일 수 있습니다.

이는 로컬 `main`이 `origin/main`보다 두 커밋 뒤에 있다는 뜻입니다.

반대로:

```text
## main...origin/main [ahead 1]
```

이면 로컬에만 존재하는 커밋이 하나 있다는 뜻입니다.

둘 다 있다면:

```text
## main...origin/main [ahead 1, behind 2]
```

처럼 표시될 수 있으며, 로컬과 원격의 이력이 갈라졌다는 뜻입니다.

---

# 불확실할 때 `pull`부터 하지 않는 이유

```bash
git pull
```

은 단순 조회 명령이 아닙니다.

개념적으로는 보통:

```text
fetch
+
merge 또는 rebase
```

입니다.

정확한 후속 동작은 Git 설정과 명령 옵션에 따라 달라집니다.

따라서 현재 상태를 모르는 상황에서 `pull`부터 실행하면 원격 상태를 확인하는 동시에 로컬 브랜치 이력까지 변경될 수 있습니다.

먼저:

```bash
git fetch origin
```

으로 정보를 갱신한 뒤:

```bash
git status --short --branch
git branch -vv
git log --oneline --decorate --graph --all
```

으로 차이를 확인하는 편이 안전합니다.

---

# 최신 기준점에서 작업 브랜치 만들기

원격 정보를 갱신합니다.

```bash
git fetch origin
```

그 뒤 작업 브랜치의 시작점을 명시적으로 `origin/main`으로 지정합니다.

```bash
git switch --no-track -c feature/title-check origin/main
```

각 부분의 의미:

```text
git switch
→ 브랜치를 전환

-c feature/title-check
→ 새 로컬 브랜치 생성

origin/main
→ 새 브랜치가 시작할 커밋

--no-track
→ origin/main을 새 브랜치의 upstream으로 자동 설정하지 않음
```

직후 상태:

```text
HEAD → feature/title-check
        │
        ▼
        C ← origin/main
```

즉:

```text
feature/title-check와 origin/main은 같은 커밋 C를 가리킴
feature/title-check의 upstream은 없음
```

확인:

```bash
git branch -vv
```

예:

```text
* feature/title-check abc1234 chore: baseline
  main                abc1234 [origin/main] chore: baseline
```

새 작업 브랜치 옆에 `[origin/main]`이 없다면 upstream이 아직 없는 상태입니다.

---

## 시작 커밋을 직접 확인하기

브랜치를 만든 뒤 단순히 "아마 `origin/main`에서 만들었을 것"이라고 기억에 의존할 필요는 없습니다.

다음으로 확인할 수 있습니다.

```bash
git rev-parse HEAD
git rev-parse origin/main
```

두 값이 같으면 현재 시점에서는 같은 커밋을 가리킵니다.

또는:

```bash
git log -1 --oneline --decorate HEAD
git log -1 --oneline --decorate origin/main
```

으로 사람이 읽기 쉬운 형태로 비교할 수 있습니다.

아직 새 커밋을 만들지 않았다면 둘이 동일해야 합니다.

---

# 최초 push와 upstream

`origin/main`은 **브랜치 생성 기준점**이지 새 작업 브랜치의 upstream으로 삼아야 하는 대상은 아닙니다.

작업 브랜치:

```text
feature/title-check
```

에 대응하는 원격 브랜치를 처음 만들 때:

```bash
git push -u origin HEAD
```

를 사용할 수 있습니다.

현재 브랜치가 `feature/title-check`라면 개념적으로:

```text
로컬:
feature/title-check

원격:
origin/feature/title-check
```

가 생기고 로컬 브랜치의 upstream이 설정됩니다.

이후:

```bash
git branch -vv
```

에서 다음처럼 확인할 수 있습니다.

```text
* feature/title-check abc1234 [origin/feature/title-check] ...
```

이제 일반적인:

```bash
git push
git pull
```

이 어느 원격 브랜치를 대상으로 하는지 Git이 알 수 있습니다.

---

# `local-git-lab`에서 확인하기

저장소 루트에서 실행합니다.

```bash
cd exercises/local-git-lab
./git-lab.sh sample
```

생성된 복제본을 조회합니다.

```bash
git -C lab/sample-app status --short --branch
git -C lab/sample-app branch -vv
git -C lab/sample-app remote -v
git -C lab/sample-app log -1 --oneline --decorate
```

`git -C <경로>`는 셸의 현재 디렉터리를 직접 바꾸지 않고 해당 경로에서 Git 명령을 실행하는 방식입니다.

즉:

```bash
git -C lab/sample-app status
```

는 개념적으로:

```bash
cd lab/sample-app
git status
```

와 비슷한 역할을 합니다.

---

## 작업 브랜치 만들기

먼저 원격 추적 정보를 갱신합니다.

```bash
git -C lab/sample-app fetch origin
```

그 뒤 `origin/main`에서 새 브랜치를 만듭니다.

```bash
git -C lab/sample-app switch --no-track \
  -c feature/local-check \
  origin/main
```

확인:

```bash
git -C lab/sample-app branch -vv
```

가능하다면 시작점도 직접 비교합니다.

```bash
git -C lab/sample-app rev-parse HEAD
git -C lab/sample-app rev-parse origin/main
```

새 커밋을 만들기 전에는 두 값이 같아야 합니다.

---

## 실습 상태 초기화

기존 실습 상태를 버려도 될 때만 실행합니다.

```bash
./git-lab.sh --reset sample
```

`--reset`이라는 이름이 붙은 실습 명령은 기존 상태를 제거하고 다시 생성할 가능성이 있으므로, 남겨야 할 실습 결과가 없는지 먼저 확인합니다.

---

# 작업 시작 점검표

```text
[ ] git rev-parse --show-toplevel 결과가 작업하려던 저장소인가?
[ ] user.name과 user.email이 현재 저장소에 맞는가?
[ ] 각 설정값이 어느 config 파일에서 왔는지 확인했는가?
[ ] origin의 fetch URL과 push URL이 모두 올바른가?
[ ] 현재 브랜치가 예상한 브랜치인가?
[ ] 현재 브랜치의 upstream이 예상한 대상인가?
[ ] git fetch origin으로 원격 추적 정보를 갱신했는가?
[ ] 작업 트리에 보존해야 할 수정이 없는가?
[ ] 인덱스에 이전 작업의 staged 변경이 없는가?
[ ] 새 브랜치가 정확히 최신 origin/main에서 시작했는가?
[ ] 새 브랜치 이름이 팀 규칙에 맞는가?
```

---

# 완료 기준

* 작업 트리, 인덱스, `HEAD`의 역할을 구분해 설명할 수 있습니다.
* `main`과 `origin/main`이 서로 다른 ref라는 것을 설명할 수 있습니다.
* `origin/main`이 실시간 원격 상태가 아니라 마지막 fetch 결과라는 것을 설명할 수 있습니다.
* `git fetch`가 원격 추적 ref를 갱신하지만 현재 로컬 브랜치를 자동으로 merge하지 않는다는 것을 설명할 수 있습니다.
* 작성자 정보와 원격 인증 계정을 구분할 수 있습니다.
* 저장소 루트, 원격 URL, 현재 브랜치, upstream, 작업 트리 상태를 명령으로 확인할 수 있습니다.
* 최신 `origin/main`에서 upstream 없는 작업 브랜치를 만들 수 있습니다.
* 브랜치를 만든 직후 `HEAD`와 `origin/main`이 같은 커밋인지 직접 확인할 수 있습니다.
* 파일을 수정하기 전에 잘못된 저장소, 잘못된 계정 설정, 남아 있는 이전 작업을 발견할 수 있습니다.