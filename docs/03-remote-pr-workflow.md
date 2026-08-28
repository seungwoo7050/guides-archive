# 원격 브랜치와 Pull Request 협업

## 목표

로컬에서 만든 작업을 원격 브랜치에 게시하고, Pull Request(PR)로 변경을 제안한 뒤, CI와 리뷰 결과를 반영해 병합 가능한 상태로 만듭니다.

전체 흐름은 다음과 같습니다.

```text
최신 기준 브랜치 확인
→ 작업 브랜치 생성
→ 목적별 커밋
→ 최초 push와 upstream 설정
→ Pull Request 생성
→ CI와 리뷰 반영
→ 병합
→ 로컬·원격 브랜치 정리
```

이 문서를 마치면 다음을 구분할 수 있어야 합니다.

* 로컬 브랜치
* 원격 저장소의 실제 브랜치
* `origin/*` 형태의 원격 추적 브랜치
* 로컬 브랜치의 upstream
* PR의 base와 head
* `fetch`, `pull`, `push`가 각각 어느 상태를 바꾸는지
* non-fast-forward push 거부가 발생하는 이유
* 리뷰 중 이력 재작성이 필요한 경우와 위험

---

## 원격 상태를 구분하기

### 로컬 브랜치, 원격 브랜치와 원격 추적 브랜치

다음 세 가지를 구분해야 합니다.

```text
feature/add-priority
→ 현재 로컬 저장소의 브랜치

원격 저장소의 feature/add-priority
→ GitHub 등의 서버에 실제 존재하는 브랜치

origin/feature/add-priority
→ 마지막 fetch 또는 push를 통해 로컬이 알고 있는
  원격 feature/add-priority의 위치
```

`origin/feature/add-priority`는 원격 서버의 브랜치 자체가 아닙니다.

개념적으로:

```text
원격 서버
feature/add-priority → 커밋 C
          │
          │ fetch
          ▼
로컬
origin/feature/add-priority → 커밋 C
```

입니다.

로컬 브랜치에서 새 커밋 D를 만들어도:

```text
로컬

feature/add-priority → D
                       ↓
                       C

origin/feature/add-priority → C
```

처럼 원격 추적 브랜치는 자동으로 이동하지 않습니다.

`push`가 성공한 뒤 원격과 관련 로컬 추적 정보가 갱신됩니다.

---

## upstream이라는 말의 의미

Git에서 로컬 브랜치의 **upstream**은 해당 브랜치가 기본적으로 비교하고 `pull` 또는 `push`할 대상으로 설정된 원격 추적 브랜치입니다.

예:

```text
로컬 브랜치
feature/add-priority

upstream
origin/feature/add-priority
```

다음으로 확인할 수 있습니다.

```bash
git branch -vv
```

예:

```text
* feature/add-priority abc1234 [origin/feature/add-priority] feat: add priority
```

여기서:

```text
feature/add-priority
→ 로컬 브랜치

origin/feature/add-priority
→ 이 로컬 브랜치의 upstream
```

입니다.

브랜치를 어디서 시작했는지와 upstream이 무엇인지는 별개의 개념입니다.

예를 들어:

```bash
git switch --no-track -c feature/add-priority origin/main
```

으로 만들었다면 시작점은 `origin/main`이지만 upstream은 없습니다.

이후:

```bash
git push -u origin HEAD
```

를 실행하면 보통 upstream은:

```text
origin/feature/add-priority
```

가 됩니다.

---

## `fetch`, `pull`, `push`

| 명령          | 주된 동작               | 로컬 브랜치                       | 작업 트리          |
| ----------- | ------------------- | ---------------------------- | -------------- |
| `git fetch` | 원격 객체와 원격 추적 ref 갱신 | 자동 이동하지 않음                   | 자동 통합하지 않음     |
| `git pull`  | fetch 후 현재 브랜치에 통합  | merge/rebase/fast-forward 가능 | 결과에 따라 바뀔 수 있음 |
| `git push`  | 로컬 ref와 객체를 원격에 게시  | 보통 그대로                       | 바꾸지 않음         |

### `git fetch`

```bash
git fetch origin
```

은 주로 다음을 갱신합니다.

```text
origin/main
origin/feature/*
원격에서 새로 확인된 객체
```

현재 로컬 브랜치는 자동으로 이동하지 않습니다.

---

### `git pull`

`git pull`은 단순한 정보 갱신 명령이 아닙니다.

개념적으로:

```text
git fetch
+
git merge
```

또는 설정에 따라:

```text
git fetch
+
git rebase
```

등으로 동작할 수 있습니다.

따라서 현재 상태가 불확실하다면 먼저:

```bash
git fetch origin
git status --short --branch
git log --oneline --decorate --graph --all -15
```

로 상태를 확인합니다.

---

### `git push`

```bash
git push
```

는 현재 로컬 변경을 단순히 "업로드"하는 명령이라기보다, **지정한 로컬 ref의 위치로 원격 ref를 이동하도록 요청하는 명령**입니다.

원격 저장소는 다음 이유 등으로 push를 거부할 수 있습니다.

* non-fast-forward
* 보호 브랜치
* 권한 부족
* 서버 정책
* 필수 서명 정책
* pre-receive hook
* 브랜치 이름 제한

따라서 로컬에서 명령이 유효하다고 해서 원격이 반드시 받아들이는 것은 아닙니다.

---

# 최신 기준 브랜치에서 작업 브랜치 만들기

먼저 원격 상태를 갱신합니다.

```bash
git fetch origin
```

그리고 최신 `origin/main`에서 작업 브랜치를 만듭니다.

```bash
git switch --no-track -c feature/add-priority origin/main
```

직후:

```text
origin/main ── C
               ↑
feature/add-priority
               ↑
              HEAD
```

상태입니다.

즉:

```text
feature/add-priority와 origin/main은 같은 커밋을 가리킴
feature/add-priority의 upstream은 없음
```

확인:

```bash
git branch -vv
git status --short --branch
git log -1 --oneline --decorate
```

---

## 작업과 커밋

작업 중에는 변경 목적별로 커밋을 만듭니다.

```bash
git status --short
git diff

git add -p
git diff --staged --check
git diff --staged

./scripts/check.sh
git commit
```

PR에서 커밋을 리뷰할 수 있다는 점 때문에도 관계없는 변경을 한 커밋에 섞지 않는 것이 중요합니다.

---

# 최초 push와 upstream 설정

로컬 작업 브랜치를 원격에 처음 게시합니다.

```bash
git push -u origin HEAD
```

현재 브랜치가:

```text
feature/add-priority
```

라면 보통 원격에:

```text
origin/feature/add-priority
```

에 해당하는 브랜치가 생성됩니다.

`-u` 또는 `--set-upstream`은 현재 로컬 브랜치와 원격 추적 브랜치를 연결합니다.

확인:

```bash
git status --short --branch
git branch -vv
```

예:

```text
## feature/add-priority...origin/feature/add-priority
```

```text
* feature/add-priority abc1234 [origin/feature/add-priority] feat: add priority
```

이제 기본 비교 대상과 일반적인 `push` 대상은 `origin/feature/add-priority`입니다.

시작점이었던 `origin/main`과 역할이 다릅니다.

```text
origin/main
→ 작업을 시작한 기준 브랜치

origin/feature/add-priority
→ 현재 작업 브랜치의 원격 대응 브랜치
```

---

# 다른 복제본이 변경을 보는 시점

개발자 A가 push했다고 해서 개발자 B의 로컬 저장소가 자동으로 바뀌지는 않습니다.

```text
A의 로컬 커밋
→ A의 push
→ 원격 브랜치 이동
→ B의 로컬 상태는 그대로
→ B가 fetch
→ B의 origin/* 갱신
```

예를 들어 A가:

```text
origin/feature/add-priority
C → D
```

로 push했더라도 B가 아직 fetch하지 않았다면 B의 로컬:

```text
origin/feature/add-priority → C
```

는 그대로일 수 있습니다.

B에서 전후를 비교합니다.

```bash
git branch -r
git log --oneline --decorate --all -12

git fetch origin

git branch -r
git log --oneline --decorate --all -12
```

따라서 다른 개발자와 대화할 때:

> "내 `origin/main`은 최신이다"

라는 표현은 마지막 fetch 시점을 함께 고려해야 합니다.

---

# Pull Request가 나타내는 관계

Pull Request는 특정 저장소 플랫폼의 협업 기능입니다. Git 자체에 PR 객체가 존재하는 것은 아닙니다.

GitHub 기준으로 보통:

```text
base: main
head: feature/add-priority
```

입니다.

의미는:

> `feature/add-priority`에 있는 변경을 `main`에 통합하자는 제안

입니다.

---

## base와 head

```text
base
→ 변경을 받아들일 대상 브랜치

head
→ 변경을 제안하는 브랜치
```

예:

```text
main
A ─ B ─ C
         \
          D ─ E
              ↑
      feature/add-priority
```

PR:

```text
base = main
head = feature/add-priority
```

라면 리뷰 대상은 일반적으로 D와 E가 만든 변경입니다.

---

# PR을 만들기 전 로컬에서 범위 확인

먼저 원격 정보를 최신으로 만듭니다.

```bash
git fetch origin
```

작업 브랜치에만 존재하는 커밋:

```bash
git log --oneline origin/main..HEAD
```

이 표현은:

```text
HEAD에서 도달 가능하지만
origin/main에서는 도달할 수 없는 커밋
```

을 보여 줍니다.

---

## PR 형태의 diff 확인

```bash
git diff --stat origin/main...HEAD
git diff origin/main...HEAD
```

여기서 `...`는 단순히 양쪽 끝을 직접 비교한다는 의미가 아닙니다.

Git은 두 ref의 **merge base**를 찾은 뒤 대략:

```text
merge-base(origin/main, HEAD)
        ↓
       HEAD
```

사이의 변경을 비교합니다.

예:

```text
A ─ B ─ C ─ F        origin/main
         \
          D ─ E      HEAD
```

merge base는 C입니다.

```bash
git diff origin/main...HEAD
```

은 개념적으로:

```text
C와 E의 차이
```

를 보여 줍니다.

이는 PR에서 "이 작업 브랜치가 공통 분기점 이후 무엇을 바꿨는가"를 확인할 때 적합합니다.

---

## `..`와 `...`를 혼동하지 않기

커밋 조회:

```bash
git log origin/main..HEAD
```

과 diff:

```bash
git diff origin/main...HEAD
```

은 비슷하게 보이지만 사용 목적이 다릅니다.

```text
git log A..B
→ B에는 있지만 A에는 없는 커밋

git diff A...B
→ A와 B의 merge base에서 B까지의 변경
```

PR 검토에서는 둘을 함께 사용하는 경우가 많습니다.

---

# PR 생성 전 점검

```text
[ ] base 저장소와 base 브랜치가 맞는가?
[ ] head 저장소와 head 브랜치가 맞는가?
[ ] 관련 없는 커밋이 섞이지 않았는가?
[ ] 관련 없는 파일이 섞이지 않았는가?
[ ] 자동 생성물이나 개인 파일이 실수로 들어가지 않았는가?
[ ] 비밀값이나 토큰이 포함되지 않았는가?
[ ] 프로젝트 검사를 통과했는가?
[ ] PR 설명과 실제 diff 범위가 일치하는가?
[ ] 의도적으로 제외한 후속 작업을 구분했는가?
```

---

# Pull Request 본문

PR 본문은 diff에 이미 보이는 파일 목록을 그대로 다시 적는 문서가 아닙니다.

리뷰어가 코드만 보고는 알기 어려운 다음 정보를 전달하는 것이 핵심입니다.

* 무엇이 문제였는가?
* 왜 이 변경이 필요한가?
* 해결 범위는 어디까지인가?
* 어떻게 검증했는가?
* 무엇을 의도적으로 하지 않았는가?

예:

```markdown
## 문제

작업 우선순위를 저장할 필드가 없어 정렬 기준을 영속적으로 유지할 수 없습니다.

## 변경

- 작업 스키마에 `priority` 필드를 추가했습니다.
- 기존 필드의 의미와 저장 형식은 변경하지 않았습니다.

## 검증

- `./scripts/check.sh`
- 기존 필수 필드 유지 확인
- 중복 필드 없음 확인

## 범위 밖

- `priority` 값의 enum 제한
- UI의 우선순위 표시
```

이 구조의 장점은 리뷰어가 빠르게 다음을 판단할 수 있다는 것입니다.

```text
문제가 실제로 존재하는가?
변경이 문제와 대응하는가?
PR이 불필요하게 커지지 않았는가?
어떤 검증이 수행됐는가?
남은 작업이 결함인지 의도적 제외인지?
```

---

# Draft Pull Request

Draft PR은 구현 완료 전에 변경 방향을 공유하는 데 사용할 수 있습니다.

적합한 경우:

* 설계 방향을 일찍 검토받고 싶음
* CI를 원격 환경에서 먼저 확인해야 함
* 큰 변경을 여러 단계로 진행 중임
* 특정 위험에 대한 피드백이 필요함
* 다른 작업과 충돌 가능성이 있어 가시성을 높여야 함

Draft는:

> 아직 검증되지 않았지만 그냥 merge해 달라

는 의미가 아닙니다.

정식 리뷰 요청 전에는 최소한 다음을 확인합니다.

```text
[ ] 최종 diff 범위를 확인했는가?
[ ] 필요한 테스트를 실행했는가?
[ ] 관련 문서와 마이그레이션을 포함했는가?
[ ] 아직 해결되지 않은 문제를 기록했는가?
[ ] 리뷰어가 특별히 확인해야 할 부분을 명시했는가?
```

---

# 리뷰 의견 반영

리뷰 수정도 일반 개발 변경과 같은 절차를 사용합니다.

```bash
# 파일 수정

git diff

./scripts/check.sh

git add -p
git diff --staged --check
git diff --staged

git commit -m "fix: address schema review"

git push
```

리뷰 중이라고 해서 검토 절차를 생략할 이유는 없습니다.

---

## 리뷰 피드백의 종류 구분

리뷰 댓글을 모두 같은 성격으로 볼 필요는 없습니다.

예:

```text
명백한 결함
→ 수정 필요

프로젝트 스타일·관례 위반
→ 일반적으로 프로젝트 규칙에 맞춰 수정

설계 질문
→ 설명으로 해결될 수도 있음

대안 제안
→ 반드시 적용해야 하는 것은 아님

범위 확대 요청
→ 현재 PR과 분리할지 판단 필요
```

리뷰 요청의 의도를 이해하지 못했다면 임의로 다른 문제를 해결하지 않습니다.

---

# 리뷰 중 새 커밋과 이력 재작성

리뷰 피드백을 반영하는 방법은 크게 두 가지가 있습니다.

### 새 커밋 추가

```text
A ─ B ─ C
        ↑
기존 PR

A ─ B ─ C ─ D
            ↑
리뷰 수정
```

장점:

* 리뷰 과정이 보존됨
* 이미 확인한 기존 커밋의 해시가 바뀌지 않음
* 일반 `git push` 가능

---

### amend 또는 rebase

예:

```bash
git commit --amend
```

또는:

```bash
git rebase -i
```

결과:

```text
기존
A ─ B ─ C

재작성
A ─ B' ─ C'
```

기존 커밋 해시가 바뀝니다.

이미 원격에 게시한 브랜치라면 일반 push로는 갱신할 수 없을 수 있습니다.

이런 방식은 다음을 확인한 뒤 사용합니다.

* 팀이 PR 브랜치의 이력 재작성을 허용하는가?
* 다른 사람이 해당 브랜치에서 작업 중이지 않은가?
* 리뷰어가 기존 커밋을 기준으로 검토 중이지 않은가?
* CI나 자동화가 특정 SHA를 참조하고 있지 않은가?

---

# CI 실패 조사

CI 실패를 단순히:

> GitHub가 이상하다

라고 처리하지 않습니다.

먼저 실패 위치를 구체화합니다.

```text
workflow
→ job
→ step
→ 실제 실행 명령
→ 종료 코드와 오류 출력
```

가능한 원인:

* 자신의 변경으로 재현되는 테스트 실패
* lint 또는 type check 실패
* 지원하지 않는 런타임 버전
* OS별 동작 차이
* 의존성 설치 실패
* 캐시 문제
* 간헐적 테스트
* 토큰 또는 비밀값 권한 부족
* fork PR에서 secret을 사용할 수 없는 구조
* 기준 브랜치 변경으로 발생한 문제
* workflow YAML 오류
* 외부 서비스 장애

---

## 조사 순서

```text
실패한 workflow 확인
→ 실패한 job 확인
→ 실패한 step 확인
→ 실제 실행 명령 확인
→ 종료 코드와 로그 확인
→ 같은 명령을 로컬에서 재현
→ HEAD와 최신 기준 브랜치 차이 확인
→ 원인 수정
→ 로컬 검증
→ push
→ 새 CI 결과 확인
```

가능하다면 CI와 같은 환경 조건도 맞춥니다.

예:

```text
런타임 버전
의존성 버전
환경 변수
운영체제
아키텍처
작업 디렉터리
```

---

## 재실행으로 통과한 경우

CI를 재실행했는데 코드 변경 없이 통과했다면:

```text
간헐적 테스트
외부 서비스 문제
네트워크 문제
일시적 runner 문제
캐시 문제
```

등을 의심할 수 있습니다.

하지만:

```text
재실행해서 통과함
=
원인이 해결됨
```

은 아닙니다.

재현 가능한 간헐 실패라면 별도 수정 대상이 될 수 있습니다.

---

# 비선형 push 거부

일반적인 push:

```bash
git push
```

가 다음과 같은 이유로 거부될 수 있습니다.

```text
원격 브랜치에
내 로컬 브랜치에는 없는 새 커밋이 존재함
```

예:

```text
공통
A ─ B

로컬
A ─ B ─ C

원격
A ─ B ─ D
```

로컬 C를 그대로 원격에 push하면 D가 원격 브랜치 이력에서 사라질 수 있으므로 Git 서버는 일반적으로 이를 거부합니다.

이것이 대표적인 non-fast-forward 상황입니다.

---

## 실패 뒤 바로 강제 push하지 않기

먼저:

```bash
git fetch origin
git status --short --branch
git log --oneline --decorate --graph --all -15
```

로 실제 그래프를 확인합니다.

예:

```text
      C   feature/add-priority
     /
A ─ B
     \
      D   origin/feature/add-priority
```

이제 D가 무엇인지 판단해야 합니다.

* 다른 사람이 만든 유효한 커밋인가?
* 내가 다른 복제본에서 push한 커밋인가?
* 자동화가 만든 커밋인가?
* 버려도 되는 잘못된 원격 이력인가?

---

# 원격 커밋을 보존하며 통합하기

### merge

```bash
git merge origin/feature/add-priority
```

예:

```text
      C
     / \
A ─ B   M
     \ /
      D
```

두 이력을 모두 보존합니다.

---

### rebase

```bash
git rebase origin/feature/add-priority
```

기존:

```text
      C
     /
A ─ B
     \
      D
```

rebase 후:

```text
A ─ B ─ D ─ C'
```

C는 새 부모를 가지는 C'로 다시 생성되므로 해시가 바뀝니다.

---

## 어느 방식을 사용할지는 팀 정책에 따른다

다음 중 하나가 절대적으로 항상 옳은 것은 아닙니다.

```text
merge
rebase
```

팀이:

* PR 브랜치에서도 merge commit을 허용하는지
* 선형 이력을 요구하는지
* 리뷰 중 force push를 허용하는지

확인해야 합니다.

---

# `--force-with-lease`

이미 원격에 게시한 커밋을 rebase하거나 amend하면 원격과 로컬의 커밋 해시가 달라집니다.

이때 일반 push가 거부될 수 있습니다.

필요하다면:

```bash
git push --force-with-lease
```

를 사용할 수 있습니다.

`--force-with-lease`는 단순 `--force`보다 안전 장치를 제공합니다.

개념적으로:

> 내가 마지막으로 확인했던 원격 브랜치 위치가 아직 그대로일 때만 강제로 갱신하라.

즉, 다른 사람이 그 사이 새 커밋을 push했다면 실패하게 만들 수 있습니다.

그래도 이것은 **원격 이력을 재작성하는 명령**입니다.

따라서:

* 공유 브랜치인지
* 리뷰어가 보고 있는지
* 팀이 허용하는지

를 먼저 확인해야 합니다.

---

# PR 병합 방식

저장소에서는 여러 병합 방식을 사용할 수 있습니다.

대표적으로:

```text
merge commit
squash merge
rebase merge
```

각 방식은 작업 브랜치 커밋이 `main`에 남는 형태가 다릅니다.

---

## merge commit

작업 브랜치 커밋이 그대로 보존되고 merge commit이 추가될 수 있습니다.

```text
A ─ B ───── M
     \     /
      C ─ D
```

---

## squash merge

PR의 여러 커밋을 하나의 새 커밋으로 합쳐 `main`에 넣습니다.

```text
작업 브랜치

A ─ B
     \
      C ─ D ─ E
```

병합 뒤:

```text
main

A ─ B ─ S
```

S는 C, D, E와 동일한 커밋이 아닙니다.

---

## rebase merge

작업 브랜치 커밋을 base 위로 다시 작성해 선형으로 붙일 수 있습니다.

```text
A ─ B ─ C' ─ D' ─ E'
```

원래 C, D, E와 해시가 달라질 수 있습니다.

이 차이는 병합 뒤 로컬 브랜치를 삭제할 때도 중요합니다.

---

# 병합 뒤 정리

먼저 원격 정보를 정리합니다.

```bash
git fetch --prune origin
```

`--prune`은 원격에서 삭제된 브랜치에 대응하는 더 이상 유효하지 않은 원격 추적 ref를 정리합니다.

예:

```text
원격에서 feature/add-priority 삭제됨
```

이라면 fetch prune 후:

```text
origin/feature/add-priority
```

도 제거될 수 있습니다.

---

## 로컬 `main` 갱신

```bash
git switch main
git merge --ff-only origin/main
```

`--ff-only`는 fast-forward가 가능한 경우에만 `main`을 이동시킵니다.

예:

```text
local main
A ─ B

origin/main
A ─ B ─ C ─ D
```

이면:

```text
main
A ─ B ─ C ─ D
```

로 단순 이동합니다.

반대로 로컬 `main`에 별도 커밋이 있어 이력이 갈라져 있으면 merge commit을 임의로 만들지 않고 실패합니다.

---

# 로컬 작업 브랜치 삭제

```bash
git branch -d feature/add-priority
```

`-d`는 안전 삭제입니다.

Git이 해당 브랜치의 커밋이 적절히 병합되지 않았다고 판단하면 삭제를 거부할 수 있습니다.

이때 바로:

```bash
git branch -D feature/add-priority
```

를 사용하지 않습니다.

먼저 확인합니다.

```bash
git branch --contains feature/add-priority
git log --oneline --decorate --graph --all -15
```

---

## squash merge 후 `-d`가 거부될 수 있는 이유

작업 브랜치:

```text
A ─ B
     \
      C ─ D
```

가 squash merge되면:

```text
main

A ─ B ─ S
```

가 됩니다.

S의 내용은 C+D일 수 있지만 Git 그래프상 C와 D가 `main`의 조상은 아닙니다.

따라서:

```bash
git branch -d feature/add-priority
```

가 "완전히 병합되지 않았다"고 판단할 수 있습니다.

이 경우:

* PR이 실제로 병합됐는가?
* 필요한 변경이 `main`에 존재하는가?
* 로컬 브랜치에 아직 보존해야 할 커밋이 있는가?

를 확인한 뒤 필요하면 강제 삭제합니다.

```bash
git branch -D feature/add-priority
```

---

# `local-git-lab`에서 여러 복제본 비교하기

실습 환경을 초기화합니다.

```bash
cd exercises/local-git-lab
./git-lab.sh --reset team
```

생성된 복제본:

```text
lab/team-app-dev-a
lab/team-app-dev-b
lab/team-app-maintainer
```

각 저장소의 현재 상태를 비교합니다.

```bash
git -C lab/team-app-dev-a branch -vv
git -C lab/team-app-dev-b branch -vv
git -C lab/team-app-maintainer branch -vv
```

그래프:

```bash
git -C lab/team-app-dev-a log \
  --oneline --decorate --graph --all

git -C lab/team-app-dev-b log \
  --oneline --decorate --graph --all

git -C lab/team-app-maintainer log \
  --oneline --decorate --graph --all
```

---

## 실습에서 확인할 내용

### A와 B가 같은 원격을 사용한다고 상태가 같은 것은 아니다

예:

```text
dev-a
→ feature/add-priority 체크아웃

dev-b
→ feature/add-assignee 체크아웃
```

두 복제본 모두 동일한 `origin` URL을 사용하더라도:

* 현재 브랜치
* 로컬 커밋
* 작업 트리
* 원격 추적 ref의 최신성

은 서로 다를 수 있습니다.

---

### `feature/add-priority`가 이미 `main`에 병합됐을 수 있다

maintainer 복제본에서는 최신 fetch 결과로 병합을 알고 있지만 dev-b는 아직 모를 수 있습니다.

```text
maintainer

origin/main → 병합 후 커밋
```

```text
dev-b

origin/main → 병합 전 커밋
```

이 차이는:

```bash
git fetch origin
```

전후로 확인할 수 있습니다.

---

### `feature/add-assignee`가 오래된 `main`에서 분기됐을 수 있다

예:

```text
A ─ B ─ C ─ D   main
     \
      E ─ F     feature/add-assignee
```

작업 브랜치는 B에서 시작했지만 `main`은 이미 D까지 진행된 상태입니다.

이 경우 PR 병합 전에 최신 base와의 충돌이나 테스트 문제를 확인해야 할 수 있습니다.

---

# 표준 협업 절차

```bash
# 1. 원격 상태 갱신
git fetch origin

# 2. 최신 기준 브랜치에서 작업 브랜치 생성
git switch --no-track \
  -c feature/TOPIC \
  origin/main

# 3. 작업과 로컬 검토
git status --short
git diff

git add -p
git diff --staged --check
git diff --staged

./scripts/check.sh
git commit

# 4. 최초 게시와 upstream 설정
git push -u origin HEAD

# 5. PR 범위 확인
git fetch origin
git log --oneline origin/main..HEAD
git diff --stat origin/main...HEAD
git diff origin/main...HEAD

# 6. 리뷰 수정
git diff
git add -p
git diff --staged
./scripts/check.sh
git commit
git push

# 7. 병합 뒤 정리
git fetch --prune origin
git switch main
git merge --ff-only origin/main

# 병합 상태 확인 후
git branch -d feature/TOPIC
```

---

# 완료 기준

* 로컬 브랜치, 실제 원격 브랜치, `origin/*` 원격 추적 브랜치를 구분할 수 있습니다.
* 브랜치를 시작한 기준점과 현재 upstream을 구분할 수 있습니다.
* `fetch`, `pull`, `push`가 어느 상태를 변경하는지 설명할 수 있습니다.
* 최초 `push -u`로 작업 브랜치의 upstream을 설정할 수 있습니다.
* PR의 base와 head 방향을 설명할 수 있습니다.
* `git log origin/main..HEAD`와 `git diff origin/main...HEAD`의 차이를 설명할 수 있습니다.
* merge base를 기준으로 PR 변경 범위를 확인할 수 있습니다.
* 리뷰 수정 시 새 커밋과 이력 재작성 중 어느 방식을 사용하는지 판단할 수 있습니다.
* CI 실패를 workflow, job, step, 명령 수준까지 좁혀 조사할 수 있습니다.
* non-fast-forward push가 왜 거부되는지 커밋 그래프로 설명할 수 있습니다.
* 강제 push 전에 원격 변경을 확인할 수 있습니다.
* `--force-with-lease`가 일반 `--force`보다 어떤 안전 장치를 제공하는지 설명할 수 있습니다.
* merge commit, squash merge, rebase merge의 이력 차이를 구분할 수 있습니다.
* 병합 뒤 원격 추적 브랜치와 로컬 작업 브랜치를 안전하게 정리할 수 있습니다.