# Git 복구 절차

## 목표

Git에서 문제가 생겼을 때 "`되돌린다`"는 표현만으로 명령을 선택하지 않습니다.

먼저 **무엇을 복구하거나 취소하려는지**, 그리고 그 변경이 **어느 상태에 존재하는지** 구분해야 합니다.

가장 먼저 다음 세 경우를 나눕니다.

```text
1. 아직 커밋하지 않은 변경인가?

2. 커밋했지만 내 로컬에만 존재하는가?

3. 이미 원격에 게시해 다른 사람과 공유된 커밋인가?
```

같은 실수라도 위치에 따라 적절한 명령이 완전히 다릅니다.

예를 들어:

```text
작업 트리 변경 취소
→ restore

로컬 커밋 위치 변경
→ reset 등을 검토

이미 공유한 커밋의 효과 취소
→ revert를 우선 검토
```

핵심 원칙은:

> 복구 작업 자체가 새로운 손실을 만들지 않도록, 현재 상태와 복구 지점을 먼저 확보한 뒤 가장 작은 범위의 명령을 선택하는 것입니다.

## 가장 먼저 할 일

문제가 발생했다고 즉시 `reset --hard`, `clean`, 강제 push부터 실행하지 않습니다.

먼저 현재 상태를 기록합니다.

```bash
git status

git branch --show-current
git branch -vv

git log --oneline --decorate --graph --all -15

git reflog -15
```

각 명령의 목적:

```text
git status
→ 작업 트리, index, 진행 중인 Git 작업 확인

git branch --show-current
→ 현재 브랜치 확인

git branch -vv
→ 브랜치 위치와 upstream 관계 확인

git log --graph --all
→ 현재 보이는 커밋 그래프 확인

git reflog
→ 최근 HEAD/ref 이동 기록 확인
```

특히 다음 작업이 중간 상태인지 확인합니다.

```text
merge in progress
rebase in progress
cherry-pick in progress
revert in progress
```

이 상태에서는 새로운 `reset` 등을 하기보다 먼저 해당 작업의:

```text
--continue
--skip
--abort
```

가능성을 검토해야 합니다.

현재 `HEAD`의 커밋을 잃을 가능성이 있으면 이름 있는 브랜치로 먼저 보존할 수 있습니다.

```bash
git branch backup/before-recovery-$(date +%Y%m%d-%H%M%S)
```

이 명령은 현재 `HEAD`가 가리키는 커밋에 새 브랜치 이름만 추가합니다.

파일이나 커밋 내용을 변경하지 않습니다.

하지만 이 백업 브랜치가 보호하는 것은 **커밋된 내용**입니다.

다음은 보호하지 않습니다.

```text
아직 커밋하지 않은 작업 트리 변경

미추적 파일

.gitignore로 무시된 파일
```

특히 중요한 미추적 파일이 있다면 별도 디렉터리에 복사하거나 다른 안전한 방법으로 보존할지 먼저 판단합니다.

## 상황별 선택표

| 상황                         | 먼저 검토할 명령                                       | 핵심 결과                     |
| -------------------------- | ----------------------------------------------- | ------------------------- |
| 스테이징하지 않은 tracked 파일 변경 취소 | `git restore FILE`                              | 작업 트리 변경 제거               |
| 스테이징만 취소하고 수정 유지           | `git restore --staged FILE`                     | index만 되돌리고 작업 트리는 유지     |
| 마지막 로컬 커밋 보완               | `git commit --amend`                            | 마지막 커밋을 새 커밋으로 교체         |
| 마지막 로컬 커밋을 다시 작업 상태로       | `git reset --soft HEAD~1` 또는 `git reset HEAD~1` | 브랜치를 이전 커밋으로 이동하면서 변경은 보존 |
| 잘못된 로컬 브랜치에 커밋             | 새 브랜치 생성 또는 `cherry-pick`                       | 먼저 잘못된 위치의 커밋을 보존         |
| 이미 공유한 잘못된 커밋의 효과 취소       | `git revert SHA`                                | 반대 변경을 새로운 커밋으로 기록        |
| reset/rebase 후 커밋이 안 보임    | `git reflog` 후 새 브랜치                            | 이전 커밋 위치를 다시 참조           |
| 진행 중인 merge/rebase 취소      | 해당 작업의 `--abort`                                | 가능하면 시작 전 상태로 복귀          |
| 미추적 파일 삭제 전 확인             | `git clean -nd`                                 | 삭제할 목록만 미리 표시             |
| push가 거부됨                  | `git fetch` 후 그래프 확인                            | 원격과 로컬 이력 차이 조사           |

이 표도 기계적인 정답은 아닙니다.

명령을 고르기 전에 다음을 확인합니다.

```text
무엇을 없애려는가?

무엇은 반드시 보존해야 하는가?

이미 다른 사람과 공유됐는가?

커밋 해시를 바꿔도 되는가?

미추적 파일도 영향을 받는가?
```

## 작업 트리 변경 복구

### 스테이징하지 않은 tracked 파일 변경 버리기

먼저 버릴 내용을 확인합니다.

```bash
git diff -- src/app.py
```

정말 필요 없는 변경이라고 확인했을 때:

```bash
git restore src/app.py
```

를 실행합니다.

기본적인 경우 이 명령은 작업 트리의 `src/app.py`를 index 상태에 맞춥니다.

따라서 스테이징하지 않은 수정은 사라집니다.

중요한 점:

```text
git restore FILE
→ 새로운 Git 커밋을 만드는 명령이 아님
→ 해당 작업 트리 수정에 reflog 복구 지점을 자동으로 만드는 명령도 아님
```

즉, 아직 어디에도 저장하지 않은 변경은 손실될 수 있습니다.

실행 전에 반드시 diff를 읽습니다.

### 스테이징만 취소하기

스테이징된 내용을 먼저 확인합니다.

```bash
git diff --staged -- src/app.py
```

스테이징만 취소합니다.

```bash
git restore --staged src/app.py
```

일반적인 경우:

```text
HEAD
→ 기준

index
→ HEAD 상태로 되돌림

working tree
→ 현재 수정 내용 유지
```

확인합니다.

```bash
git status --short

git diff -- src/app.py
git diff --staged -- src/app.py
```

예상되는 상태는:

```text
git diff
→ 수정 내용 존재

git diff --staged
→ 해당 파일의 스테이징 변경 없음
```

입니다.

## 로컬 커밋 복구

### 마지막 커밋에 누락 추가

아직 다른 사람에게 공유하지 않은 마지막 커밋이라면 amend를 사용할 수 있습니다.

```bash
# 파일 수정

git add path/to/file

git diff --staged

git commit --amend --no-edit
```

`--no-edit`은 기존 커밋 메시지를 그대로 사용한다는 뜻입니다.

중요한 점은:

```text
기존 커밋을 내부에서 수정
```

하는 것이 아니라:

```text
기존 부모
+
새 tree
+
커밋 메타데이터
→ 새로운 commit object 생성
```

이라는 것입니다.

따라서 amend 전후 커밋 SHA는 달라집니다.

이미 게시한 커밋이라면 단순한 "수정"이 아니라 이력 재작성이 되므로 별도로 판단해야 합니다.

### 마지막 커밋을 다시 나누기

하나의 로컬 커밋에 서로 다른 목적의 변경을 잘못 묶었다고 가정합니다.

먼저 현재 커밋을 보존합니다.

```bash
git branch backup/before-split
```

마지막 커밋을 없애되 해당 변경 전체를 index에 유지합니다.

```bash
git reset --soft HEAD~1
```

개념적으로:

```text
reset 전

A──B
   ↑
 branch

reset --soft HEAD~1 후

A
↑ branch

B의 변경
→ index와 working tree에 유지
```

다시 목적별로 선택하려면 우선 index를 비웁니다.

```bash
git restore --staged .
```

이제 작업 트리에 변경은 남아 있고 index는 기준 커밋 상태가 됩니다.

그 후:

```bash
git add -p

git diff --staged

git commit
```

을 반복해 여러 커밋으로 나눌 수 있습니다.

옵션 없는:

```bash
git reset HEAD~1
```

은 기본적으로 mixed reset입니다.

개념적으로:

```text
브랜치
→ 이전 커밋으로 이동

index
→ 이전 커밋 상태

working tree
→ 기존 변경 유지
```

따라서 `--soft`와의 주요 차이는 index를 유지하는지 여부입니다.

```text
--soft
→ index 유지

mixed(default)
→ index도 대상 커밋 기준으로 재설정

--hard
→ index와 tracked working tree까지 대상 커밋 기준으로 변경
```

## 잘못된 브랜치에 커밋

예를 들어 `main`에 있어야 하지 않는 작업 커밋을 실수로 만들었다고 가정합니다.

가장 중요한 것은 **먼저 그 커밋을 잃지 않도록 이름을 붙이는 것**입니다.

현재 잘못 만든 커밋이 `HEAD`라면:

```bash
git switch -c feature/correct-topic
```

만으로 현재 커밋을 새 브랜치가 가리키게 할 수 있습니다.

예:

```text
실수 직후:

A──B
   ↑
 main
 HEAD

새 브랜치 생성 후:

A──B
   ↑
 main
 feature/correct-topic
 HEAD
```

이후 `main`을 어디로 되돌릴지는 해당 커밋이 이미 공유됐는지에 따라 별도로 처리합니다.

이미 올바른 목적의 브랜치가 존재한다면 커밋 SHA를 기록하고 해당 브랜치로 이동한 뒤:

```bash
git switch feature/correct-topic
git cherry-pick COMMIT_SHA
```

을 사용할 수 있습니다.

`cherry-pick`은 해당 커밋 객체 자체를 이동시키는 것이 아니라 그 커밋이 만든 변경을 현재 브랜치 위에 다시 적용해 새로운 커밋을 생성합니다.

따라서 일반적으로 원본과 새 커밋의 SHA는 다릅니다.

## 공유한 커밋 취소

이미 원격에 게시해 다른 사람과 공유한 커밋은 일반적으로 이력에서 제거하기보다 **반대 변경을 새 커밋으로 기록**하는 방식을 먼저 검토합니다.

```bash
git fetch origin

git show BAD_COMMIT_SHA

git revert BAD_COMMIT_SHA
```

예를 들어:

```text
A──B──C
```

에서 `C`가 잘못된 커밋이라면 revert 후:

```text
A──B──C──R
```

이 됩니다.

`R`은 `C`를 삭제하는 커밋이 아닙니다.

```text
C의 변경 효과를 반대로 적용하는 새로운 커밋
```

입니다.

따라서 기존 `C`는 이력에 그대로 남고 공유된 커밋 해시도 유지됩니다.

revert 중 충돌이 발생하면:

```bash
git status

# 충돌 해결

git add path/to/resolved-file

git revert --continue
```

를 사용합니다.

취소하려면:

```bash
git revert --abort
```

합니다.

## merge commit을 revert할 때

merge commit은 부모가 둘 이상이므로 단일 부모 커밋과 다르게 처리해야 합니다.

먼저 구조를 확인합니다.

```bash
git show --no-patch --pretty=raw MERGE_COMMIT_SHA
```

예를 들어:

```text
parent AAA
parent BBB
```

처럼 두 부모가 나타납니다.

merge revert에서는 어떤 부모를 mainline으로 간주할지 지정해야 합니다.

```bash
git revert -m 1 MERGE_COMMIT_SHA
```

`-m 1`은:

```text
첫 번째 부모를 기준 상태로 유지하면서
merge를 통해 들어온 다른 쪽 변경 효과를 되돌려라
```

는 의미입니다.

하지만:

```text
merge commit이면 무조건 -m 1
```

이 아닙니다.

실제 부모 관계와 어느 방향의 변경을 제거하려는지 확인해야 합니다.

잘못된 mainline을 선택하면 의도와 다른 변경을 되돌릴 수 있습니다.

## 진행 중인 작업 중단

Git이 특정 작업의 중간 상태라면 작업 종류에 맞는 abort 명령을 사용합니다.

```bash
git merge --abort

git rebase --abort

git cherry-pick --abort

git revert --abort
```

일반적으로 목적은:

```text
현재 진행 중인 작업을 취소하고
작업 시작 전 상태로 복원
```

하는 것입니다.

반면 일부 Git 작업에는 `--quit`도 존재합니다.

`--quit`은 보통:

```text
진행 중이라는 관리 상태는 종료하지만
현재 index와 working tree 상태는 그대로 둘 수 있음
```

이라는 점에서 `--abort`와 다릅니다.

즉:

```text
abort
→ 작업 자체를 되돌리고 싶음

quit
→ Git의 진행 상태만 종료하고 현재 변경은 남기고 싶음
```

으로 구분해 생각합니다.

## reflog에서 커밋 찾기

`git log`에서 커밋이 사라졌다고 해서 Git 객체가 즉시 삭제된 것은 아닙니다.

Git은 로컬에서 `HEAD`와 여러 ref가 이동한 기록을 reflog에 남깁니다.

```bash
git reflog --date=local -30
```

예:

```text
abc1234 HEAD@{0}: reset: moving to HEAD~2
def5678 HEAD@{1}: commit: add parser
...
```

reset이나 rebase 전에 `HEAD`가 가리키던 커밋을 여기서 찾을 수 있습니다.

후보를 확인합니다.

```bash
git show CANDIDATE_SHA
```

원하는 커밋이라면 즉시 이름 있는 브랜치로 보존합니다.

```bash
git branch recovery/lost-work CANDIDATE_SHA
```

이제 해당 커밋은 명시적인 branch ref가 가리키므로 이후 작업에서 찾기 쉽습니다.

reflog의 한계도 이해해야 합니다.

```text
각 로컬 저장소마다 별도로 존재

GitHub의 전역 복구 기록이 아님

영구 보존을 보장하지 않음

Git의 만료·정리 정책에 따라 오래된 항목이 사라질 수 있음
```

따라서 필요한 커밋을 찾았다면 reflog 위치만 기억하지 말고 브랜치나 태그 등 명시적인 ref로 보존합니다.

## detached `HEAD` 커밋 보존

특정 커밋을 직접 checkout하거나 switch해 detached `HEAD` 상태에서 작업할 수 있습니다.

이 상태에서 커밋을 만들면:

```text
HEAD
 ↓
새 커밋

브랜치
→ 새 커밋을 가리키지 않을 수 있음
```

이후 다른 브랜치로 이동하면 새 커밋이 일반적인 `git log`에서 보이지 않게 될 수 있습니다.

이동하기 전에 현재 SHA를 기록할 수 있습니다.

```bash
git rev-parse HEAD
```

예:

```text
SAVED_SHA=<현재 SHA>
```

브랜치로 이동한 뒤:

```bash
git switch main
git branch recovery/detached SAVED_SHA
```

처럼 이름을 붙일 수 있습니다.

더 간단하게 아직 detached commit 위에 있는 상태라면 바로:

```bash
git switch -c recovery/detached
```

처럼 새 브랜치를 만드는 방법도 있습니다.

핵심은:

```text
중요한 커밋에 이름 있는 ref를 연결한다
```

입니다.

## stash 사용

작업 트리 변경을 임시로 치워야 할 때 stash를 사용할 수 있습니다.

추적 중인 변경과 미추적 파일을 함께 stash하려면:

```bash
git stash push -u -m 'work before rebase'
```

`-u`는 untracked 파일도 포함합니다.

일반적인 ignored 파일까지 자동으로 포함하는 것은 아닙니다.

저장된 stash를 확인합니다.

```bash
git stash list
```

특정 stash의 변경 요약:

```bash
git stash show --stat 'stash@{0}'
```

적용하되 stash 자체는 남기려면:

```bash
git stash apply --index 'stash@{0}'
```

`--index`는 가능하면 stash 당시의 staged 상태도 복원하려는 옵션입니다.

적용 결과를 확인한 뒤 더 이상 필요 없다면 직접 삭제합니다.

```bash
git stash drop 'stash@{0}'
```

`pop`은 개념적으로:

```text
stash 적용
+
성공적으로 적용되면 stash 제거
```

를 한 번에 수행합니다.

```bash
git stash pop
```

충돌이 발생하면 stash가 실제로 제거됐는지 추측하지 말고:

```bash
git stash list
git status
```

로 확인합니다.

stash는 짧은 임시 전환에는 편리하지만 중요한 장기 작업의 주 저장 수단으로 사용하기에는 불리합니다.

중요한 작업은 가능하면:

```text
브랜치 생성
+
명시적인 커밋
```

으로 보존하는 편이 추적과 복구가 쉽습니다.

## `reset --hard`와 `clean`

두 명령 모두 손실 가능성이 크므로 목적과 대상이 다르다는 점을 구분해야 합니다.

### `reset --hard`

예:

```bash
git reset --hard TARGET
```

일반적으로 다음을 `TARGET` 커밋 상태에 맞춥니다.

```text
현재 브랜치
index
tracked working tree files
```

즉, 커밋하지 않은 tracked 파일 변경을 잃을 수 있습니다.

실행 전에 최소한 다음을 확인합니다.

```bash
git status --short

git diff

git diff --staged

git log --oneline --decorate -10
```

현재 `HEAD` 커밋을 보존해야 한다면:

```bash
git branch backup/before-hard-reset
```

을 만들 수 있습니다.

하지만 다시 강조하면 이 브랜치는:

```text
커밋된 내용
```

만 보호합니다.

작업 트리에만 있는 변경을 보호하지 않습니다.

따라서 `reset --hard` 전에 가장 중요한 질문은:

```text
작업 트리와 index에 아직 커밋하지 않은 필요한 변경이 없는가?
```

입니다.

### `clean`

`git clean`은 tracked 파일이 아니라 **untracked 파일과 디렉터리**를 삭제하는 데 사용됩니다.

먼저 dry-run을 실행합니다.

```bash
git clean -nd
```

의미:

```text
-n
→ 실제 삭제하지 않고 예정된 항목만 표시

-d
→ untracked directory도 대상에 포함
```

무시된 파일까지 포함해 어떤 항목이 삭제될지 보려면:

```bash
git clean -ndx
```

를 사용할 수 있습니다.

`-x`는 `.gitignore` 등의 ignore 규칙까지 무시하고 대상에 포함합니다.

실제 삭제는 목록을 확인한 뒤에만 검토합니다.

```bash
git clean -fd
```

특히 다음은 매우 주의해야 합니다.

```bash
git clean -fdx
```

이 명령은 프로젝트가 의도적으로 Git에서 제외한 다음 파일까지 삭제할 수 있습니다.

```text
로컬 .env

IDE 설정

빌드 결과

dependency cache

개인 테스트 데이터

로컬 인증 설정
```

따라서 `clean`은 반드시 dry-run 결과를 먼저 확인합니다.

## 잘못된 강제 push

공유 브랜치에 잘못된 force push를 수행했다면 추가적인 덮어쓰기를 막는 것이 우선입니다.

권장되는 사고 순서:

```text
1. 해당 브랜치에 추가 push 중단

2. 팀원에게 현재 브랜치를 건드리지 않도록 공유

3. force push 전 커밋 SHA 탐색

4. 후보 커밋을 별도 브랜치로 보존

5. 현재 원격 SHA 확인

6. 어떤 SHA를 복구해야 하는지 팀에서 합의

7. 예상 원격 SHA를 조건으로 복구
```

이전 SHA는 다음 장소에 남아 있을 수 있습니다.

```text
force push를 하기 전 개발자의 reflog

아직 fetch하지 않은 다른 개발자의 origin/BRANCH

해당 커밋을 직접 가지고 있는 다른 복제본

CI나 배포 시스템이 기록한 SHA

Pull Request나 코드 리뷰 기록
```

복구 후보를 찾으면 즉시:

```bash
git branch recovery/pre-force-push RECOVERY_SHA
```

처럼 보존합니다.

현재 원격 상태도 확인합니다.

```bash
git fetch origin
git rev-parse origin/BRANCH
```

팀에서 복구할 커밋과 현재 원격 커밋을 확인한 뒤 필요하다면:

```bash
git push \
  --force-with-lease=BRANCH:CURRENT_REMOTE_SHA \
  origin RECOVERY_SHA:BRANCH
```

처럼 현재 원격 상태에 조건을 걸어 복구할 수 있습니다.

핵심은 개인 판단으로 공유 브랜치를 연속해서 강제 수정하지 않는 것입니다.

잘못된 force push 이후 또 다른 force push를 반복하면 복구에 사용할 수 있는 최신 복제본과 상태까지 빠르게 사라질 수 있습니다.

## 비밀값을 커밋한 경우

비밀번호, API token, private key 등의 비밀값을 Git에 커밋했다면 **Git 이력에서 문자열을 지우는 것보다 자격 증명을 무효화하는 것이 먼저**입니다.

이미 원격에 push했다면 노출된 것으로 간주합니다.

우선순위:

```text
토큰 폐기 또는 교체

비밀번호 변경

SSH/API 키 폐기와 재발급

관련 세션 또는 자격 증명 무효화

접근 로그 확인

보안 담당자와 저장소 관리자에게 알림
```

왜냐하면 Git 이력에서 비밀값을 나중에 삭제하더라도 이미 다음 장소에 복사됐을 수 있기 때문입니다.

```text
다른 개발자의 clone

fork

CI 로그 또는 cache

artifact

백업

검색 index

이미 비밀값을 읽은 제3자
```

최신 커밋에서 파일을 삭제하는 것만으로도 충분하지 않습니다.

예:

```text
커밋 A
→ secret 포함

커밋 B
→ secret 파일 삭제
```

여전히 `A`에는 secret이 존재합니다.

이력에서 제거해야 한다면 repository history rewrite가 필요할 수 있지만, 이는 clone, fork, open PR, tag, 배포 시스템 등에 영향을 줄 수 있습니다.

따라서 저장소 관리자와 영향 범위를 확인한 뒤 별도 절차로 진행합니다.

## `local-git-lab`의 `recovery` 상태 확인

실습 상태를 다시 만듭니다.

```bash
cd exercises/local-git-lab

./git-lab.sh --reset recovery

cd lab/recovery-lab
```

전체 그래프와 복구 관련 상태를 확인합니다.

```bash
git log --oneline --decorate --graph --all

git reflog

git branch --list 'recovery/*'

git stash list
```

reset 전에 보존한 브랜치의 파일을 확인합니다.

```bash
git show recovery/reset:reset.txt
```

이 명령은 현재 작업 트리를 바꾸지 않고 해당 커밋의 특정 파일 내용을 읽습니다.

detached `HEAD`에서 만든 작업:

```bash
git show recovery/detached:detached.txt
```

`revert` 전후 tree 자체가 같은지 비교할 수도 있습니다.

```bash
git rev-parse HEAD~2^{tree}
git rev-parse HEAD^{tree}
```

두 값이 같다면 두 커밋의 **최종 파일 트리 내용**이 동일하다는 의미입니다.

하지만 이것이 두 커밋의 SHA가 같다는 뜻은 아닙니다.

```text
commit object
→ 부모, 작성자, 시간, 메시지, tree 등을 포함

tree object
→ 특정 시점의 디렉터리와 파일 구조
```

따라서 revert를 통해 파일 상태가 과거와 같아져도 새로운 commit history는 남습니다.

stash가 보존한 경로를 확인합니다.

```bash
git stash show --name-only 'stash@{0}'
```

`-u`로 stash한 untracked 파일은 stash 내부에서 별도 부모 형태로 저장될 수 있으므로 실습 저장소에서는 다음과 같이 확인할 수 있습니다.

```bash
git ls-tree -r --name-only 'stash@{0}^3'
```

다만 stash 내부 표현은 사용자가 일상적인 복구 절차에서 직접 조작하기 위한 안정적인 고수준 인터페이스라기보다 Git 객체 구조를 확인하는 실습 용도로 이해하는 편이 좋습니다.

## 복구 후 검증

복구 명령이 성공했다는 메시지만 보고 작업을 끝내지 않습니다.

최종 상태를 다시 확인합니다.

```bash
git status --short --branch

git branch -vv

git log --oneline --decorate --graph --all -15

git diff

git diff --staged

# 프로젝트가 지정한 검사 실행
```

최소한 다음을 확인합니다.

```text
[ ] 필요한 커밋이 이름 있는 브랜치나 다른 ref로 보존됐는가?

[ ] 현재 브랜치가 의도한 커밋을 가리키는가?

[ ] 작업 트리와 index가 예상한 상태인가?

[ ] 필요한 미추적 파일을 잃지 않았는가?

[ ] 다른 사람이 만든 원격 커밋을 제거하지 않았는가?

[ ] upstream 관계가 예상대로 유지되는가?

[ ] 프로젝트 테스트와 검사가 통과하는가?
```

복구의 완료 기준은 단순히 Git 명령이 오류 없이 끝난 것이 아닙니다.

```text
필요한 개발 이력 보존
+
의도한 파일 상태 복구
+
공유 이력 안전성 확인
+
프로젝트 검증 성공
```

까지 확인해야 합니다.

## 완료 기준

* 작업 트리에만 있는 변경, index에 있는 변경, 로컬 커밋과 이미 공유한 커밋을 구분할 수 있습니다.
* `restore`, `reset`, `revert`가 각각 어떤 상태를 대상으로 하는지 설명할 수 있습니다.
* `reset --soft`, 기본 mixed reset과 `reset --hard`의 차이를 설명할 수 있습니다.
* 공유된 잘못된 커밋에서 `reset`보다 `revert`를 먼저 검토하는 이유를 설명할 수 있습니다.
* reflog가 무엇을 기록하며 왜 영구적인 백업으로 간주하면 안 되는지 설명할 수 있습니다.
* reflog에서 잃어버린 커밋을 찾고 이름 있는 브랜치로 보존할 수 있습니다.
* detached `HEAD`에서 만든 커밋을 브랜치로 보존할 수 있습니다.
* stash에서 tracked, staged, untracked 상태가 어떻게 다뤄지는지 확인할 수 있습니다.
* `git clean`이 tracked 파일이 아니라 untracked 파일을 대상으로 한다는 점을 설명할 수 있습니다.
* `reset --hard`, `clean`, force push를 실행하기 전에 각각 어떤 데이터가 손실될 수 있는지 판단할 수 있습니다.
* 잘못된 force push 이후 추가 변경을 멈추고 기존 SHA를 확보한 뒤 조건부 복구를 수행할 수 있습니다.
* 비밀값을 push한 경우 Git 이력 정리보다 자격 증명 폐기와 교체가 우선인 이유를 설명할 수 있습니다.
