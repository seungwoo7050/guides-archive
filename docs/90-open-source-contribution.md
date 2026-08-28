
# 오픈소스에 작은 변경 기여하기

이 과정은 기본적인 Git 브랜치 협업과 Pull Request, CI 사용법을 익힌 뒤 진행하는 선택 과정입니다.

회사 내부 저장소와 달리 외부 오픈소스에서는 보통 다음이 추가됩니다.

```text
원본 저장소
내 fork
프로젝트별 기여 규칙
공개 커뮤니케이션
CLA 또는 DCO
외부 유지관리자의 리뷰
```

핵심은 코드를 많이 바꾸는 것이 아니라 **프로젝트의 기존 규칙을 존중하면서 작고 검증 가능한 변경을 제안하는 것**입니다.

---

## 목표

* 원본 저장소와 자신의 fork를 구분합니다.
* `origin`과 `upstream`의 일반적인 역할을 이해합니다.
* 프로젝트의 기여 규칙과 검증 명령을 변경 전에 확인합니다.
* 기준 상태가 이미 실패하는 경우 자신의 변경과 구분합니다.
* 하나의 문제만 해결하는 작은 변경을 만듭니다.
* CLA, DCO sign-off, 암호학적 커밋 서명을 구분합니다.
* fork에서 원본 저장소로 PR을 올바른 방향으로 생성합니다.
* upstream 변경과 리뷰 피드백을 안전하게 반영합니다.

---

# 수정하기 전에 읽을 파일

저장소 루트와 `.github/`를 확인합니다.

대표적인 파일:

```text
README.md
CONTRIBUTING.md
SECURITY.md
CODE_OF_CONDUCT.md
LICENSE
LICENSE.md
.github/ISSUE_TEMPLATE/*
.github/PULL_REQUEST_TEMPLATE*
```

프로젝트에 따라 다음도 중요할 수 있습니다.

```text
DEVELOPMENT.md
HACKING.md
GOVERNANCE.md
SUPPORT.md
MAINTAINERS
CODEOWNERS
```

---

## 각 파일에서 확인할 내용

| 파일              | 확인할 내용                     |
| --------------- | -------------------------- |
| README          | 프로젝트 목적, 지원 환경, 기본 빌드·테스트  |
| CONTRIBUTING    | 기여 절차, 이슈·브랜치·커밋·PR 규칙     |
| SECURITY        | 보안 취약점의 비공개 신고 방법          |
| Code of Conduct | 커뮤니티에서 요구하는 행동 기준          |
| LICENSE         | 코드와 문서의 이용·배포 조건           |
| Issue 템플릿       | 버그 재현과 기능 요청에 필요한 정보       |
| PR 템플릿          | 검증, 관련 이슈, 체크리스트 등 PR 요구사항 |
| CI 설정           | 실제 자동 검증 명령과 지원 환경         |

---

## `CONTRIBUTING.md`가 없을 때

기여 문서가 없다고 해서 아무 방식으로 작업해도 된다는 뜻은 아닙니다.

다음을 확인합니다.

* 최근 병합된 PR
* 최근 유지관리자 리뷰
* CI workflow
* 커밋 제목 관례
* 릴리스 방식
* Issue 라벨
* 기존 `good first issue`
* 같은 종류의 이전 변경

특히 큰 구조 변경은 먼저 논의하는 편이 안전합니다.

---

# 보안 문제는 공개 PR로 시작하지 않기

다음과 같은 것을 발견했다면:

* 인증 우회
* 원격 코드 실행
* 비밀값 노출
* 권한 상승
* 민감한 사용자 데이터 노출

공개 Issue나 PR에 재현 코드를 바로 게시하면 실제 악용 가능성을 높일 수 있습니다.

먼저:

```text
SECURITY.md
GitHub Security Advisory
프로젝트가 지정한 보안 이메일
별도 신고 포털
```

등의 비공개 절차를 확인합니다.

보안 수정 절차는 일반적인 버그 수정 PR과 다를 수 있습니다.

---

# 첫 기여 범위 고르기

처음 기여에서는 **작고 경계가 명확한 문제**가 적합합니다.

좋은 후보:

* 재현 가능한 작은 버그
* 명백한 문서 오류
* 깨진 링크
* 기존 동작을 고정하는 작은 테스트
* 유지관리자가 표시한 `good first issue`
* 작은 오류 처리 누락
* 공개 API를 바꾸지 않는 국소적 정리

---

## 먼저 논의하는 편이 좋은 변경

* 공개 API 변경
* 데이터 형식 변경
* 저장 형식 또는 프로토콜 변경
* 새 주요 기능
* 의존성 대규모 교체
* 빌드 시스템 교체
* 전역적인 이름 변경
* 대규모 formatter 적용
* 폴더 구조 재설계
* 지원 플랫폼 변경
* 호환성 정책 변경

이런 변경은 구현 난이도보다 **프로젝트 방향성에 대한 합의**가 더 중요할 수 있습니다.

---

# 작업 전에 기존 논의 확인

다음을 확인합니다.

```text
같은 Issue가 이미 있는가?
같은 PR이 열려 있는가?
누군가 이미 작업하겠다고 표시했는가?
유지관리자가 선호하는 해결 방법을 말했는가?
구현 전에 RFC나 설계 논의를 요구하는가?
문제를 재현할 수 있는가?
완료 기준이 명확한가?
```

중복 작업은 기술적으로 올바르더라도 병합되지 않을 가능성이 높습니다.

---

# fork, `origin`, `upstream`

fork 기반 오픈소스 기여의 일반적인 구조는 다음과 같습니다.

```text
원본 저장소
original-owner/repository
        ↑
      upstream
        │
로컬 복제본
        │
      origin
        ↓
내 fork
your-account/repository
```

보통:

```text
origin
→ 내가 push 권한을 가진 내 fork

upstream
→ 실제 프로젝트의 원본 저장소
```

로 사용합니다.

단, `origin`과 `upstream`은 단순한 remote 이름일 뿐 Git이 의미를 강제하지는 않습니다. 팀이나 개인이 다른 이름을 사용할 수도 있습니다.

---

# fork 복제와 upstream 추가

먼저 GitHub에서 원본 저장소를 fork합니다.

그 뒤 자신의 fork를 복제합니다.

```bash
git clone https://github.com/YOUR_ACCOUNT/REPOSITORY.git
cd REPOSITORY
```

원본 저장소를 `upstream`으로 추가합니다.

```bash
git remote add upstream \
  https://github.com/ORIGINAL_OWNER/REPOSITORY.git
```

확인:

```bash
git remote -v
```

예:

```text
origin    https://github.com/me/project.git (fetch)
origin    https://github.com/me/project.git (push)
upstream  https://github.com/project/project.git (fetch)
upstream  https://github.com/project/project.git (push)
```

실제 권한이 없다면 `upstream`의 push URL이 표시되더라도 push는 거부될 수 있습니다.

---

# 현재 로컬 상태 확인

```bash
git branch -vv
git status --short --branch
git remote -v
```

확인할 내용:

```text
origin이 정말 내 fork인가?
upstream이 정말 원본인가?
현재 브랜치는 무엇인가?
현재 작업 트리는 깨끗한가?
현재 main은 어느 remote를 추적하는가?
```

---

# 최신 upstream에서 브랜치 만들기

원본 프로젝트의 최신 기준 상태를 가져옵니다.

```bash
git fetch upstream
```

작업 브랜치를 만듭니다.

```bash
git switch --no-track \
  -c fix/documentation-link \
  upstream/main
```

직후:

```text
upstream/main
      ↑
fix/documentation-link
      ↑
     HEAD
```

이며 작업 브랜치에는 upstream이 없습니다.

이후 자신의 fork에 게시합니다.

```bash
git push -u origin HEAD
```

이제:

```text
로컬:
fix/documentation-link

upstream:
origin/fix/documentation-link
```

관계가 됩니다.

주의할 점은 이름이 헷갈릴 수 있다는 것입니다.

여기서 Git 용어의 **upstream branch**는:

```text
origin/fix/documentation-link
```

일 수 있지만 remote 이름 `upstream`은 원본 저장소를 뜻합니다.

즉:

```text
remote 이름 "upstream"
```

과:

```text
로컬 브랜치의 upstream
```

은 서로 다른 개념입니다.

---

# 변경 전 기준 검증

코드를 고치기 전에 프로젝트의 기존 상태를 먼저 검증합니다.

프로젝트가 지정한:

* 설치
* 빌드
* 테스트
* lint
* type check
* formatter check
* 생성 파일 검증

등을 실행합니다.

예:

```bash
./scripts/check.sh
```

또는 프로젝트 문서에 지정된 명령을 사용합니다.

---

## 기록할 내용

```text
운영체제
CPU 아키텍처가 관련 있다면 아키텍처
언어·런타임 버전
패키지 관리자 버전
중요 의존성 버전
실행한 정확한 명령
성공 또는 실패 결과
기존 실패 여부
```

특히 기준 브랜치가 이미 실패하는 경우 중요합니다.

---

# 기존 실패와 새 실패를 구분하기

예를 들어 변경 전:

```text
테스트 100개 중 1개 실패
```

변경 후:

```text
테스트 100개 중 동일한 1개 실패
```

라면 자신의 변경으로 새 실패가 추가됐다고 단정할 수 없습니다.

반면:

```text
변경 전 1개 실패
변경 후 3개 실패
```

라면 새 실패 2개는 자신의 변경과 연관됐을 가능성을 조사해야 합니다.

PR에는 필요하면 다음처럼 적습니다.

```text
기준 브랜치에서도 test_x가 실패했습니다.
이번 변경 후에도 동일하게 재현되며 새 실패는 확인되지 않았습니다.
```

원래 작업과 관계없는 기존 실패를 같은 PR에서 임의로 고치면 PR 범위가 흐려질 수 있습니다.

---

# 작은 변경 만들기

기본 원칙:

* 합의한 문제만 수정합니다.
* 관련 없는 정리 작업을 섞지 않습니다.
* 기존 스타일을 따릅니다.
* 기존 테스트 위치와 구조를 따릅니다.
* 동작 변경에는 가능한 범위의 테스트를 추가합니다.
* 프로젝트가 요구하는 생성 파일은 함께 갱신합니다.
* 필요한 문서나 마이그레이션을 PR을 작게 보이게 하려고 제외하지 않습니다.
* 불필요한 전역 formatter 적용을 피합니다.

---

## "작은 PR"의 의미

작은 PR은 단순히 파일 수가 적다는 뜻이 아닙니다.

예를 들어 DB 스키마 변경이:

```text
코드 1개
마이그레이션 1개
테스트 2개
문서 1개
```

를 필요로 한다면 모두 포함해야 완전한 변경일 수 있습니다.

반대로 한 파일에서:

```text
버그 수정
+
함수 이름 변경
+
포맷 정리
+
주석 재작성
```

을 동시에 하면 파일 수는 하나라도 리뷰 범위는 큽니다.

따라서 기준은:

> 하나의 문제를 완결성 있게 해결하는 최소한의 관련 변경

입니다.

---

# 커밋 전 검토

```bash
git status --short
git diff

git add -p

git diff --staged --check
git diff --staged

# 프로젝트가 요구하는 검사
./scripts/check.sh

git commit
```

PR보다 먼저 로컬 커밋 자체가 검토 가능한 상태인지 확인합니다.

---

# CLA, DCO와 커밋 서명

세 가지는 서로 다른 목적을 가집니다.

---

## CLA

CLA는 Contributor License Agreement입니다.

프로젝트에 따라 기여자가:

* 개인 CLA
* 기업 CLA

등에 동의해야 할 수 있습니다.

보통:

* GitHub App
* 별도 웹 페이지
* 전자 서명 서비스

등을 통해 처리합니다.

CLA의 목적은 프로젝트가 기여 코드를 어떤 조건으로 사용할 수 있는지를 법적으로 명확히 하는 것입니다.

Git 커밋 명령 자체의 기능은 아닙니다.

---

# DCO와 sign-off

DCO는 Developer Certificate of Origin입니다.

프로젝트가 DCO를 사용하는 경우 커밋 메시지에 다음 trailer를 요구할 수 있습니다.

```text
Signed-off-by: Seungwoo Kim <name@example.com>
```

Git에서는:

```bash
git commit -s
```

로 추가할 수 있습니다.

예:

```text
fix: update documentation link

Signed-off-by: Seungwoo Kim <name@example.com>
```

`-s`는 **암호학적 서명 기능이 아닙니다.**

의미는 대략:

> 이 기여를 제출할 권리가 있으며 프로젝트의 DCO 취지에 동의한다.

는 선언을 커밋 메시지에 기록하는 것입니다.

정확한 법적 의미는 프로젝트가 채택한 DCO 문서를 확인해야 합니다.

---

# GPG 또는 SSH 커밋 서명

```bash
git commit -S
```

는 커밋 객체에 암호학적 서명을 추가합니다.

지원 환경에 따라 GPG, SSH 등의 방식이 사용될 수 있습니다.

목적은:

```text
이 커밋이 해당 서명 키를 가진 주체에 의해 서명되었는지 검증
```

하는 것입니다.

따라서 다음은 별개입니다.

```text
CLA
→ 법적 기여 계약

DCO sign-off
→ Signed-off-by trailer를 통한 기여 권한 선언

commit signing
→ 암호학적 서명
```

프로젝트가 둘 이상을 동시에 요구할 수도 있습니다.

예:

```bash
git commit -s -S
```

처럼 사용할 수도 있습니다.

---

# Pull Request 방향 확인

fork 기반 PR은 저장소까지 포함해서 네 항목을 확인해야 합니다.

```text
base 저장소:
original-owner/repository

base 브랜치:
main

head 저장소:
your-account/repository

head 브랜치:
fix/documentation-link
```

GitHub UI에서는 head 쪽이 "compare" 브랜치로 표시되기도 합니다.

방향이 뒤집히면 원본 저장소의 거대한 diff를 자신의 fork에 병합하려는 이상한 PR이 될 수 있습니다.

---

# PR 전 로컬 확인

원본 기준을 최신으로 가져옵니다.

```bash
git fetch upstream
```

커밋 확인:

```bash
git log --oneline upstream/main..HEAD
```

변경 확인:

```bash
git diff --stat upstream/main...HEAD
git diff upstream/main...HEAD
```

이 경우 PR의 base가 원본의 `main`이므로 `origin/main`보다 `upstream/main`이 더 정확한 비교 기준입니다.

---

# 오픈소스 PR 본문

예:

```markdown
## 문제

설치 문서의 링크가 이전 위치를 가리켜 현재 404가 발생합니다.

## 변경

- 링크를 현재 공식 문서 주소로 변경했습니다.
- 주변 설명과 문서 구조는 변경하지 않았습니다.

## 검증

- 프로젝트의 문서 검사 실행
- 렌더링 결과 확인
- 새 링크의 응답 확인

## 범위 밖

- 설치 절차 전체 재작성
- 주변 문서 표현 정리
```

리뷰어가 확인해야 하는 것은:

```text
정말 문제인가?
해결 방법이 최소 범위인가?
기존 스타일을 따르는가?
어떻게 검증했는가?
관련 없는 변경이 없는가?
```

입니다.

---

# upstream 변경 반영

작업 중 원본 `main`이 진행될 수 있습니다.

먼저:

```bash
git fetch upstream
```

으로 최신 상태를 가져옵니다.

현재 그래프를 확인합니다.

```bash
git log --oneline --decorate --graph --all -15
```

---

## merge 방식

```bash
git merge upstream/main
```

기존 작업 커밋을 그대로 유지하면서 최신 원본 변경을 병합합니다.

---

## rebase 방식

```bash
git rebase upstream/main
```

자신의 작업 커밋을 최신 `upstream/main` 위에 다시 생성합니다.

예:

```text
기존

A ─ B ─ C       upstream/main
     \
      D ─ E     작업 브랜치
```

최신 upstream이:

```text
A ─ B ─ C ─ F
```

까지 갔다면 rebase 후:

```text
A ─ B ─ C ─ F ─ D' ─ E'
```

가 될 수 있습니다.

D와 E는 D', E'로 다시 생성되므로 해시가 바뀝니다.

---

# 이미 fork에 게시한 상태에서 rebase한 경우

기존 원격:

```text
origin/fix/documentation-link
→ D ─ E
```

로컬 rebase 후:

```text
→ D' ─ E'
```

가 되면 일반 push는 거부될 수 있습니다.

프로젝트와 리뷰 상황이 허용한다면:

```bash
git push --force-with-lease
```

가 필요할 수 있습니다.

하지만 리뷰어가 이미 특정 커밋을 검토하고 있다면 불필요한 이력 재작성은 리뷰를 어렵게 만들 수 있습니다.

프로젝트가 명시적으로:

* PR 커밋을 깔끔하게 rebase할 것
* 리뷰 수정 시 force push할 것

등을 요구하지 않는다면 기존 관례를 먼저 확인합니다.

---

# 리뷰 반영

리뷰 댓글은 성격을 구분합니다.

```text
명백한 버그
프로젝트 규칙 위반
누락된 테스트
누락된 문서

→ 일반적으로 수정 대상
```

```text
왜 이 방식을 선택했는가?
이 대안은 검토했는가?

→ 먼저 설명이 필요한 질문
```

```text
이 PR과 무관한 다른 기능도 추가하면 어떤가?

→ 범위 확대 여부를 논의
```

```text
개인적 선호에 가까운 대안

→ 프로젝트 관례와 기술적 근거를 기준으로 판단
```

---

## 수정 절차

```bash
git diff

# 수정

git diff

git add -p
git diff --staged --check
git diff --staged

./scripts/check.sh

git commit
git push
```

리뷰 답변에는 필요하면 다음을 명확히 합니다.

```text
무엇을 수정했는가?
어떤 커밋에서 수정했는가?
왜 해당 대안을 사용했는가?
검증 결과는 무엇인가?
```

---

# 의견에 동의하지 않는 경우

오픈소스 리뷰에서 모든 제안을 무조건 받아들일 필요는 없습니다.

다만 다음 방식이 좋습니다.

```text
관찰 가능한 사실
→ 기술적 근거
→ 현재 선택의 이유
→ 가능한 대안
```

예:

```text
현재 구현은 기존 parser의 오류 처리 방식과 동일하게 -EINVAL을 반환합니다.
새 오류 타입을 추가하면 공개 API 변경이 필요하므로 이번 PR에서는 기존 규칙을 유지했습니다.
별도 오류 타입이 필요하다면 후속 변경으로 분리할 수 있습니다.
```

감정적 표현이나 유지관리자 의도 추측보다 기술적 근거가 중요합니다.

---

# 병합 뒤 정리

원본 상태를 최신으로 만듭니다.

```bash
git fetch --prune upstream
```

로컬 `main`으로 전환합니다.

```bash
git switch main
```

원본 `main`에 맞춥니다.

```bash
git merge --ff-only upstream/main
```

현재 local `main`이 upstream보다 뒤에만 있다면 fast-forward됩니다.

---

# 작업 브랜치 삭제

```bash
git branch -d fix/documentation-link
```

안전 삭제가 거부되면 먼저 확인합니다.

```bash
git log --oneline --decorate --graph --all -15
git branch --contains fix/documentation-link
```

특히 원본 프로젝트가 squash merge를 사용했다면 작업 커밋이 `upstream/main`의 조상으로 직접 들어가지 않았으므로 `-d`가 실패할 수 있습니다.

병합이 완료됐고 보존할 로컬 작업이 없음을 확인한 경우에만:

```bash
git branch -D fix/documentation-link
```

를 고려합니다.

---

# PR이 닫혔지만 병합되지 않은 경우

브랜치를 즉시 삭제하기 전에 판단합니다.

```text
후속 수정 후 다시 열 가능성이 있는가?
유지관리자가 다른 접근을 요청했는가?
일부 커밋을 다른 PR에서 재사용할 가치가 있는가?
학습용 또는 기록용으로 보존할 필요가 있는가?
```

필요하다면:

* 별도 로컬 브랜치
* patch 파일
* 다른 새 브랜치

등으로 보존할 수 있습니다.

예:

```bash
git format-patch upstream/main..fix/documentation-link
```

---

# fork 브랜치 정리

원격 fork의 작업 브랜치도 필요 없다면 삭제할 수 있습니다.

```bash
git push origin --delete fix/documentation-link
```

그 뒤:

```bash
git fetch --prune origin
```

으로 로컬 원격 추적 ref를 정리할 수 있습니다.

GitHub에서 PR 병합 시 자동으로 head 브랜치를 삭제하는 옵션을 사용하는 프로젝트도 있습니다.

---

# 표준 오픈소스 기여 절차

```bash
# 1. 원격 확인
git remote -v

# 2. 원본 최신 상태 가져오기
git fetch upstream

# 3. 원본 기준으로 작업 브랜치 생성
git switch --no-track \
  -c fix/TOPIC \
  upstream/main

# 4. 변경 전 기준 검증
./scripts/check.sh

# 5. 작업과 로컬 검토
git status --short
git diff

git add -p
git diff --staged --check
git diff --staged

./scripts/check.sh
git commit

# 프로젝트가 DCO를 요구한다면
# git commit -s

# 6. 자신의 fork에 게시
git push -u origin HEAD

# 7. 원본 기준 PR 범위 확인
git fetch upstream
git log --oneline upstream/main..HEAD
git diff --stat upstream/main...HEAD
git diff upstream/main...HEAD

# 8. 리뷰 수정
git diff
git add -p
git diff --staged
./scripts/check.sh
git commit
git push

# 9. 병합 뒤 원본 동기화
git fetch --prune upstream
git switch main
git merge --ff-only upstream/main

# 10. 브랜치 상태 확인 후 삭제
git branch -d fix/TOPIC
```

---

# 완료 기준

* 원본 저장소, 자신의 fork, 로컬 복제본의 관계를 설명할 수 있습니다.
* remote 이름 `origin`, `upstream`과 로컬 브랜치의 upstream 개념을 구분할 수 있습니다.
* 자신의 fork가 `origin`, 원본 프로젝트가 `upstream`인 일반적인 구조를 설정할 수 있습니다.
* 최신 `upstream/main`에서 작업 브랜치를 만들 수 있습니다.
* 코드 수정 전에 프로젝트의 기존 테스트 상태를 확인할 수 있습니다.
* 기존 실패와 자신의 변경이 만든 실패를 구분해 기록할 수 있습니다.
* 하나의 문제를 완결성 있게 해결하는 작은 diff를 만들 수 있습니다.
* 프로젝트의 기여 문서와 최근 관례를 변경 전에 확인할 수 있습니다.
* 보안 취약점을 공개 PR로 먼저 게시하면 안 되는 이유를 설명할 수 있습니다.
* CLA, DCO sign-off, GPG·SSH 커밋 서명을 서로 구분할 수 있습니다.
* `git commit -s`와 `git commit -S`의 차이를 설명할 수 있습니다.
* fork PR의 base 저장소, base 브랜치, head 저장소, head 브랜치를 올바르게 선택할 수 있습니다.
* `upstream/main...HEAD`를 기준으로 실제 PR diff를 확인할 수 있습니다.
* 원본 저장소의 새 변경을 merge 또는 rebase로 반영할 수 있습니다.
* 게시한 브랜치를 rebase했을 때 왜 `--force-with-lease`가 필요할 수 있는지 설명할 수 있습니다.
* 리뷰 요청을 결함, 프로젝트 관례, 설계 질문, 범위 확대 요청으로 구분할 수 있습니다.
* PR 병합 또는 종료 뒤 로컬 브랜치와 fork 브랜치를 안전하게 정리할 수 있습니다.
