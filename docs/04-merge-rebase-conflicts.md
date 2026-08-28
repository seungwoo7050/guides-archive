# merge, rebase와 충돌 해결 

## 목표

* `merge`와 `rebase`가 커밋 그래프를 어떻게 바꾸는지 설명합니다.
* 충돌이 발생했을 때 `ours`나 `theirs` 한쪽을 기계적으로 선택하지 않고 양쪽 변경의 의도를 확인합니다.
* 충돌 해결 방향이 잘못됐거나 불확실하면 작업을 중단하고 시작 전 상태로 돌아갑니다.
* `rebase`처럼 커밋 이력을 다시 작성한 뒤 일반 `push`가 거부되는 이유와 안전하게 원격을 갱신하기 위한 조건을 설명합니다.

## 분기된 그래프 읽기

공통 커밋 `B`에서 `main`과 `feature`가 갈라졌다고 가정합니다.

```text
A──B──C        main
    \
     D──E      feature
```

여기서:

```text
B
→ 두 브랜치의 공통 조상

C
→ main에서 추가된 커밋

D, E
→ feature에서 추가된 커밋
```

두 브랜치의 변경을 통합할 때 대표적으로 `merge`와 `rebase`를 선택할 수 있습니다.

### merge

`feature` 브랜치에서 `main`을 merge하면 기존 커밋을 그대로 유지하면서 두 이력을 연결합니다.

```text
A──B──C────M   feature
    \      /
     D────E
```

`M`은 두 부모를 가진 merge commit입니다.

```text
첫 번째 부모
→ merge를 실행하기 직전 feature의 E

두 번째 부모
→ 병합한 main의 C
```

특징:

* 기존 `C`, `D`, `E` 커밋을 새로 만들지 않으므로 해시가 유지됩니다.
* fast-forward가 불가능한 일반적인 분기 상태에서는 두 부모를 가진 merge commit `M`이 생성됩니다.
* 어느 시점에서 브랜치가 갈라졌고 다시 통합됐는지가 그래프에 남습니다.
* 이미 공유한 기존 커밋의 이력을 다시 쓰지 않습니다.

단, 모든 `merge`가 merge commit을 만드는 것은 아닙니다.

예를 들어 현재 브랜치가 대상 브랜치의 조상이라면 fast-forward가 가능합니다.

```text
A──B        main
    \
     C──D   feature
```

`main`에서 `feature`를 merge하면:

```text
A──B──C──D  main
```

처럼 브랜치 포인터만 앞으로 이동할 수 있습니다.

따라서:

```text
merge
≠
항상 merge commit 생성
```

입니다.

### rebase

`feature`를 `main` 위로 rebase하면 `D`, `E`의 **변경 내용**을 `C` 뒤에 다시 적용합니다.

rebase 전:

```text
A──B──C        main
    \
     D──E      feature
```

rebase 후:

```text
A──B──C──D'──E'   feature
```

중요한 점은 `D`, `E` 자체가 이동하는 것이 아니라는 것입니다.

Git은 개념적으로:

```text
D가 B에 적용한 변경
E가 D에 적용한 변경
```

을 구한 뒤:

```text
C 위에 D의 변경 적용 → D'
D' 위에 E의 변경 적용 → E'
```

처럼 새로운 커밋을 만듭니다.

따라서:

* `D'`, `E'`는 새로운 commit object입니다.
* 원래 `D`, `E`와 부모가 다르므로 해시도 달라집니다.
* 원래 `D`, `E`는 현재 브랜치의 새 이력에서는 더 이상 사용되지 않습니다.
* 이미 원격에 게시했던 `D`, `E`를 rebase하면 로컬과 원격 이력이 서로 달라집니다.

즉:

```text
merge
→ 기존 이력을 연결

rebase
→ 기존 변경을 새로운 기준점 위에서 새 커밋으로 재생성
```

이라고 이해할 수 있습니다.

## 선택 기준

| 상황                                | 먼저 검토할 선택                         |
| --------------------------------- | --------------------------------- |
| 여러 사람이 직접 사용하는 공유 브랜치             | `merge` 또는 팀이 정한 비재작성 방식          |
| 아직 push하지 않은 개인 브랜치               | `rebase` 가능                       |
| 작성자 한 명만 사용하는 PR 브랜치              | 팀 규칙과 현재 리뷰 상태를 확인한 뒤 `rebase` 가능 |
| 실제 분기와 통합 구조를 그래프에 남기고 싶음         | `merge` 검토                        |
| 기준 브랜치의 최신 커밋 뒤에 내 커밋을 다시 정렬하고 싶음 | `rebase` 검토                       |

`merge는 안전하고 rebase는 깔끔하다`처럼 단순화해서 외우지 않습니다.

더 중요한 판단 기준은 다음과 같습니다.

```text
이 커밋이 이미 다른 사람에게 공유됐는가?

다른 사람이 이 브랜치를 기반으로 작업하고 있는가?

커밋 해시가 바뀌어도 되는가?

팀에서 작업 브랜치의 이력 재작성을 허용하는가?

현재 리뷰가 특정 커밋 해시를 기준으로 진행 중인가?
```

특히 이미 여러 사람이 사용하는 브랜치를 rebase하면 다른 사람의 기존 이력과 새 이력이 갈라져 추가적인 복구 작업이 필요할 수 있습니다.

## 충돌이 발생하는 이유

Git은 단순히 두 최종 파일만 비교하지 않습니다.

일반적으로 다음 세 상태를 바탕으로 각 브랜치가 공통 조상에서 무엇을 변경했는지 판단합니다.

```text
공통 조상
현재 쪽 변경
통합하려는 쪽 변경
```

예를 들어 공통 조상의 파일이 다음과 같다고 가정합니다.

```text
title
status
```

한쪽에서는:

```text
title
status
priority
```

다른 쪽에서는:

```text
title
status
assignee
```

로 변경했습니다.

이 두 변경이 서로 다른 위치라면 Git이 자동으로 다음처럼 합칠 수도 있습니다.

```text
title
status
priority
assignee
```

따라서:

```text
두 브랜치가 같은 파일을 수정함
≠
반드시 충돌
```

입니다.

충돌은 Git이 두 변경을 자동으로 결합할 **유일하고 안전한 결과를 결정할 수 없을 때** 발생합니다.

대표적인 경우:

* 같은 줄을 서로 다르게 수정함
* 한쪽은 파일을 삭제하고 다른 쪽은 수정함
* 파일 이동과 수정이 복잡하게 겹침
* 같은 주변 문맥을 서로 다른 구조로 재작성함

충돌은 Git이 고장 난 상태가 아닙니다.

다음 판단을 개발자에게 넘긴 상태입니다.

```text
각 변경은 왜 필요했는가?

어느 변경을 유지해야 하는가?

두 변경을 모두 보존해야 하는가?

새로운 제3의 결과를 만들어야 하는가?

최종 파일의 문법과 의미가 유효한가?

프로젝트 검사가 통과하는가?
```

## `local-git-lab`에서 rebase 충돌 만들기

기존 `team` 실습 상태를 버려도 되는지 확인한 뒤 초기화합니다.

```bash
cd exercises/local-git-lab
./git-lab.sh --reset team
cd lab/team-app-dev-b
```

현재 그래프와 원격 상태를 먼저 확인합니다.

```bash
git fetch origin
git log --oneline --decorate --graph --all -15
```

`feature/add-assignee`는 이전 `main`에서 분기했고 최신 `origin/main`에는 `priority` 필드가 추가된 상태입니다.

현재 작업 브랜치를 최신 `origin/main` 위로 rebase합니다.

```bash
git rebase origin/main
```

충돌이 발생하면 즉시 파일부터 수정하지 말고 현재 상태를 확인합니다.

```bash
git status
git diff
```

`git status`는 다음을 알려 줍니다.

```text
현재 rebase가 진행 중인지

어느 커밋을 다시 적용하고 있는지

어떤 파일이 충돌 상태인지

해결 뒤 어떤 명령을 실행해야 하는지
```

rebase 중에는 새 기준점 쪽 파일과 현재 다시 적용 중인 커밋의 내용을 직접 비교할 수 있습니다.

```bash
git show HEAD:config/task-fields.yml
git show REBASE_HEAD:config/task-fields.yml
```

개념적으로:

```text
HEAD
→ 현재 rebase 기준 위에서 이미 만들어진 상태

REBASE_HEAD
→ 지금 다시 적용하려다 충돌한 원래 커밋
```

다만 충돌 상황에서 `HEAD`, index stage, `MERGE_HEAD`, `REBASE_HEAD` 등의 의미는 작업 종류에 따라 달라집니다.

따라서 `ours = 내 것`, `theirs = 상대방 것`이라고 사람 기준으로 고정해서 외우지 않습니다.

특히 rebase에서는 `ours`와 `theirs`의 관점이 일반적인 merge에서 기대한 것과 반대로 느껴질 수 있습니다.

항상 실제 내용을 확인합니다.

```bash
git status
git diff
git show HEAD:path/to/file
git show REBASE_HEAD:path/to/file
```

## 두 변경을 보존해 해결하기

이번 충돌에서는 `priority`와 `assignee` 모두 필요한 변경이라고 판단했다고 가정합니다.

최종 파일을 직접 다음처럼 만듭니다.

```yaml
fields:
  - title
  - status
  - priority
  - assignee
```

중요한 점은 충돌 표시를 단순히 삭제하는 것이 아니라 **프로젝트가 요구하는 최종 상태를 직접 작성하는 것**입니다.

충돌 표시가 남았거나 잘못된 공백이 있는지 확인합니다.

```bash
git diff --check
```

프로젝트 검사를 실행합니다.

```bash
./scripts/check.sh
```

해결한 파일을 index에 올려 Git에 충돌이 해결됐음을 알립니다.

```bash
git add config/task-fields.yml
```

상태를 다시 확인합니다.

```bash
git status
git diff --staged
```

여기서 `git add`는 단순히 "다음 커밋에 파일을 넣는다"는 의미뿐 아니라 충돌 상황에서는:

```text
이 파일의 충돌 해결 결과를 확정했다
```

는 의미도 가집니다.

모든 충돌이 해결됐다면 rebase를 계속합니다.

```bash
GIT_EDITOR=true git rebase --continue
```

`GIT_EDITOR=true`는 실습에서 커밋 메시지 편집기를 열지 않고 기존 메시지를 그대로 사용하기 위한 방법입니다.

일반적인 환경에서는 다음만 실행해도 됩니다.

```bash
git rebase --continue
```

rebase가 여러 커밋을 다시 적용하는 경우 이후 커밋에서도 추가 충돌이 발생할 수 있습니다.

그때마다:

```text
상태 확인
→ 의도 파악
→ 파일 해결
→ 검사
→ git add
→ git rebase --continue
```

를 반복합니다.

완료한 뒤 확인합니다.

```bash
./scripts/check.sh
git status --short --branch
git log --oneline --decorate --graph --all -15
```

특히 다음을 확인합니다.

```text
feature 브랜치가 최신 origin/main 위에 놓였는가?

기존 기능 변경이 모두 남아 있는가?

프로젝트 검사가 통과하는가?

새 로컬 커밋 해시가 원격 브랜치의 기존 해시와 달라졌는가?
```

## 해결하지 않고 취소하기

충돌을 반드시 해결해야 하는 것은 아닙니다.

다음과 같은 경우에는 중단하는 것이 더 안전합니다.

```text
잘못된 기준 브랜치에 rebase함

충돌 해결 의도를 판단할 정보가 부족함

예상보다 많은 커밋이 재작성됨

다른 사람과 공유된 브랜치임을 뒤늦게 확인함

현재 접근 방식 자체가 잘못됐다고 판단함
```

rebase를 취소하려면:

```bash
git rebase --abort
```

Git은 가능한 범위에서 rebase 시작 전 상태로 복원합니다.

확인합니다.

```bash
git status --short --branch
git log --oneline --decorate --graph --all -12
```

rebase 전에 관련 없는 작업 트리 변경이 없는 상태를 유지하면 `--abort` 후 결과를 판단하기 훨씬 쉽습니다.

merge를 중단하려면:

```bash
git merge --abort
```

마찬가지로 시작 전 상태로 돌아가는 것이 목적입니다.

## rebase 뒤 일반 push가 거부되는 이유

rebase 전에 로컬과 원격 브랜치가 같은 커밋을 가리키고 있었다고 가정합니다.

```text
A──B──D──E

         ↑
local feature
origin/feature
```

이후 `main`의 `C` 위로 rebase하면:

```text
A──B──C──D'──E'   local feature

    \
     D──E          origin/feature
```

가 됩니다.

원격의 `E`에서 로컬의 `E'`로 단순히 포인터를 앞으로 이동할 수 없습니다.

즉:

```text
E가 E'의 조상이 아님
```

이므로 fast-forward가 아닙니다.

따라서 일반 push:

```bash
git push
```

는 원격 이력을 우발적으로 덮어쓰는 것을 막기 위해 거부됩니다.

실패한 뒤 즉시 강제 push하지 않습니다.

먼저 원격 상태를 새로 확인합니다.

```bash
git fetch origin
git log --oneline --decorate --graph --all -15
```

다음 조건을 검토합니다.

```text
[ ] 이 브랜치를 현재 다른 사람이 직접 사용하지 않는가?

[ ] 팀이 이 PR 브랜치의 이력 재작성을 허용하는가?

[ ] 기존 리뷰에서 커밋 해시 변경이 문제가 되지 않는가?

[ ] 필요한 경우 리뷰어에게 이력 재작성을 알렸는가?

[ ] fetch 이후 원격 브랜치에 예상하지 않은 새 커밋이 없는가?

[ ] 필요한 기존 커밋을 다른 브랜치나 reflog에서 복구할 수 있는가?
```

조건이 충족될 때 `--force-with-lease`를 검토합니다.

```bash
git push --force-with-lease origin HEAD:feature/add-assignee
```

일반적인 `--force`와 중요한 차이가 있습니다.

```text
--force
→ 현재 원격 브랜치가 무엇을 가리키는지와 관계없이
  갱신을 강제로 요청할 수 있음

--force-with-lease
→ 내가 예상하고 있는 원격 상태와 실제 원격 상태가
  일치하는 경우에만 강제 갱신
```

예상한 이전 SHA를 직접 명시하면 조건을 더 명확하게 만들 수 있습니다.

```bash
git push \
  --force-with-lease=feature/add-assignee:EXPECTED_OLD_SHA \
  origin HEAD:feature/add-assignee
```

이 명령은:

```text
원격 feature/add-assignee가
EXPECTED_OLD_SHA를 가리키고 있을 때만
새 HEAD로 바꿔라
```

는 의미입니다.

그러나 `--force-with-lease`가 판단하는 것은 **원격 ref의 예상 상태**뿐입니다.

다음을 판단하지는 않습니다.

```text
이 브랜치를 다시 써도 되는 팀 규칙인가?

다른 개발자가 이 이력에 의존하고 있는가?

리뷰어에게 재작성 사실을 알려야 하는가?

업무적으로 강제 push가 허용되는가?
```

따라서:

```text
--force-with-lease가 성공할 수 있음
≠
그 push가 조직적으로 올바름
```

입니다.

## 같은 상황을 merge로 처리하기

같은 분기 상황을 rebase 대신 merge로 해결할 수 있습니다.

`team` 환경을 다시 만든 뒤 개발자 B의 브랜치에서:

```bash
git fetch origin
git merge origin/main
```

을 실행합니다.

충돌이 발생하면 해결 원칙은 동일합니다.

```bash
git status

# 양쪽 변경 의도 확인
# 최종 파일 직접 수정

./scripts/check.sh
git diff --check

git add config/task-fields.yml

git status
git diff --staged

git merge --continue
```

merge에서는 기존 작업 브랜치의 커밋을 새 커밋으로 다시 만들지 않습니다.

예:

```text
        C
       / \
A──B──D──E──M
```

실제 구조는 분기 방향에 따라 다르게 그려질 수 있지만 핵심은:

```text
기존 C, D, E
→ 해시 유지

새로운 M
→ 양쪽 이력을 연결
```

입니다.

따라서 기존 작업 브랜치가 이미 원격에 게시된 상태에서도 merge commit을 추가한 뒤 일반적인 fast-forward push가 가능한 경우가 많습니다.

## 충돌 해결 표준 절차

```bash
# 현재 작업 종류와 충돌 파일 확인
git status
git diff

# 필요한 경우 각 참조의 실제 파일 확인
git show HEAD:path/to/file

# MERGE_HEAD 또는 REBASE_HEAD가 존재하는 상황이라면 확인
git show MERGE_HEAD:path/to/file
git show REBASE_HEAD:path/to/file

# 최종 파일을 직접 작성

# 문법, 테스트와 diff 검사
./scripts/check.sh
git diff --check

# 해결된 파일을 index에 기록
git add path/to/file

# 실제 해결 결과 확인
git diff --staged
git status

# 작업 종류에 맞게 계속
git rebase --continue
# 또는
git merge --continue

# 방향이 잘못됐다면 중단
git rebase --abort
# 또는
git merge --abort
```

모든 명령을 기계적으로 실행할 필요는 없습니다.

핵심 흐름은 다음입니다.

```text
현재 어떤 작업 중인지 확인
→ 어떤 커밋과 변경이 충돌했는지 확인
→ 양쪽 변경 의도 파악
→ 올바른 최종 결과 작성
→ 프로젝트 검증
→ 해결 상태를 index에 기록
→ 계속하거나 중단
```

## 피해야 할 처리

* 충돌 표시 `<<<<<<<`, `=======`, `>>>>>>>`만 삭제하고 동작 검증을 생략하지 않습니다.
* `ours`, `theirs`를 특정 개발자 A/B로 고정해서 외우지 않습니다.
* `Accept Current`, `Accept Incoming` 같은 편집기 버튼을 의미 확인 없이 누르지 않습니다.
* 작업 트리에 관련 없는 변경이 남은 상태에서 merge나 rebase를 시작하지 않습니다.
* 일반 push가 거부됐다는 이유만으로 `--force`를 사용하지 않습니다.
* 자동 생성 파일만 충돌 해결하고 실제 원본 source/schema를 빠뜨리지 않습니다.
* 충돌 파일이 컴파일된다는 이유만으로 의미적 충돌까지 해결됐다고 판단하지 않습니다.
* rebase가 끝났다는 이유만으로 원격 브랜치를 즉시 강제 갱신하지 않습니다.

## 완료 기준

* 같은 분기 상태에 `merge`와 `rebase`를 적용했을 때 각각 어떤 커밋 그래프가 만들어지는지 그릴 수 있습니다.
* rebase에서 기존 커밋이 이동하는 것이 아니라 새로운 부모를 가진 새 커밋이 생성되는 이유를 설명할 수 있습니다.
* 동일 파일 수정과 Git conflict가 같은 개념이 아님을 설명할 수 있습니다.
* 실제 충돌에서 양쪽 변경의 목적을 확인하고 필요한 변경을 모두 보존한 최종 결과를 만들 수 있습니다.
* `git add`가 충돌 해결 과정에서 어떤 의미를 가지는지 설명할 수 있습니다.
* 잘못 시작한 merge나 rebase를 `--abort`로 중단할 수 있습니다.
* rebase 후 일반 push가 non-fast-forward로 거부되는 이유를 그래프로 설명할 수 있습니다.
* `--force-with-lease`가 검사하는 Git 상태와 검사하지 않는 팀 정책을 구분할 수 있습니다.