# Pull Request CI와 GitHub Actions 보안

## 목표

Pull Request 화면에 CI가 표시된다는 사실만으로 안전한 협업이 완성되는 것은 아닙니다.

다음 세 가지를 구분해야 합니다.

```text
CI가 실행됨

CI가 올바른 커밋을 검사함

CI 성공이 실제 병합 조건으로 강제됨
```

또한 Pull Request 코드는 외부 사용자가 작성한 신뢰하지 않는 코드일 수 있습니다.

따라서 다음 흐름 전체를 확인합니다.

```text
브랜치 push
→ Pull Request 갱신
→ workflow run 생성
→ 어떤 commit/ref가 검사되는지 확인
→ CI 결과
→ 리뷰와 실패 조사
→ 필수 상태 검사 통과
→ 병합
```

그리고 CI가 실행되는 동안:

```text
어떤 token이 있는가?

어떤 secret에 접근할 수 있는가?

신뢰하지 않는 코드가 그 권한으로 실행되는가?
```

까지 확인해야 합니다.

## Pull Request에서 무엇을 검사하는가

`pull_request` 이벤트에서 무엇이 checkout되는지는 일반적인 branch `push` 실행과 다를 수 있습니다.

Pull Request CI에서는 GitHub가 PR head와 base를 통합한 결과를 검사할 수 있도록 synthetic merge ref를 제공하는 경우가 있습니다.

개념적으로:

```text
base: main

A──B──C

head: feature

A──B──D──E
```

GitHub가 테스트용 merge 결과를 만들면:

```text
A──B──C────M
    \      /
     D────E
```

의 `M`에 해당하는 상태를 검사할 수 있습니다.

목적은 단순히:

```text
feature 자체에서 테스트 성공
```

만 보는 것이 아니라:

```text
현재 main에 feature를 통합했을 때도 테스트 성공
```

하는지 확인하는 것입니다.

따라서 다음 두 문장은 다릅니다.

```text
내 feature branch HEAD에서는 테스트가 성공한다.

현재 base branch와 통합한 PR 상태에서도 테스트가 성공한다.
```

## 실패한 PR 실행에서 확인할 것

* 이벤트가 `pull_request`인지 `push`인지
* base 저장소와 base 브랜치는 무엇인지
* head 저장소와 head 브랜치는 무엇인지
* workflow run이 표시하는 SHA는 무엇인지
* checkout step이 실제 어떤 ref를 checkout했는지
* 실행 당시 base branch가 어느 commit이었는지
* 이전 실행 이후 base branch가 변경됐는지

PR에 새 commit을 push하지 않았더라도 base branch가 바뀌면 통합 결과가 달라질 수 있습니다.

예:

```text
어제
main + feature → 성공

오늘
main에 새 commit 추가
→ main + 같은 feature → 실패 가능
```

## 필수 상태 검사

워크플로가 실행된다는 것과 실패한 워크플로가 병합을 실제로 막는다는 것은 별개입니다.

예:

```text
PR CI 실패

하지만 branch protection 없음

→ 사용자가 merge할 수 있을 수도 있음
```

실제 병합 정책은 GitHub ruleset 또는 branch protection 설정에서 구성해야 합니다.

대표적으로 확인할 항목:

```text
[ ] 보호 대상 base branch가 맞는가?

[ ] 필요한 CI check를 required status check로 지정했는가?

[ ] 최신 base와 동기화된 branch만 merge하도록 요구하는가?

[ ] 필요한 리뷰 승인 수는 몇 개인가?

[ ] stale approval을 무효화하는가?

[ ] 관리자 우회가 가능한가?

[ ] force push가 허용되는가?

[ ] branch 삭제가 허용되는가?
```

### job 이름과 required check의 관계

필수 상태 검사는 특정 check 이름을 기준으로 설정될 수 있습니다.

따라서 workflow에서:

```yaml
jobs:
  test:
```

를 나중에:

```yaml
jobs:
  verify:
```

처럼 바꾸면 저장소의 required status check 설정과 맞지 않을 수 있습니다.

즉, CI job 이름 변경은 단순한 YAML 리팩터링이 아닐 수 있습니다.

다음도 함께 검토합니다.

```text
workflow 이름
job 이름
ruleset
required status checks
```

## CI 실패 처리

### 먼저 실패 유형을 분류한다

CI 실패 원인을 무조건 애플리케이션 코드 문제로 보지 않습니다.

대표적인 분류:

* 소스 코드 오류
* 테스트 실패
* workflow YAML 문법 오류
* Action 다운로드 실패
* dependency 다운로드 실패
* runner 환경 문제
* OS 차이
* 권한 부족
* secret 미제공
* network 문제
* flaky test
* base branch 변경
* GitHub 서비스 장애

### 조사 순서

```text
workflow run의 이벤트와 SHA 확인

→ 실패한 job 확인

→ 실패한 step 확인

→ 실제 실행 명령 확인

→ 최초의 의미 있는 오류 확인

→ 같은 명령을 로컬에서 실행

→ base와 head 상태 비교

→ 원인 수정

→ 로컬 검증

→ push

→ 새 workflow run 확인
```

### 재실행은 원인 분석을 대신하지 않는다

같은 commit의 workflow를 다시 실행했는데 성공했다고 가정합니다.

```text
1차 실행 → 실패

rerun
→ 성공
```

이것만으로 문제 해결이라고 판단하면 안 됩니다.

가능성:

```text
flaky test

일시적인 network 장애

외부 package registry 오류

GitHub-hosted runner 장애

외부 API 불안정
```

특히 같은 commit과 같은 workflow인데 결과가 달랐다면 재현성이 부족한 원인을 의심해야 합니다.

## `GITHUB_TOKEN` 최소 권한

GitHub Actions는 각 workflow run에 사용할 수 있는 `GITHUB_TOKEN`을 제공합니다.

이 token은 workflow가 GitHub API나 저장소에 접근할 때 사용할 수 있습니다.

읽기 전용 CI라면:

```yaml
permissions:
  contents: read
```

정도로 충분한 경우가 많습니다.

### 권한은 실제 작업에 맞춘다

예:

```text
checkout + test
→ contents: read

PR에 자동 댓글 작성
→ pull-requests: write 필요

release 생성
→ contents: write가 필요할 수 있음

package 게시
→ packages: write가 필요할 수 있음
```

읽기 전용 테스트와 쓰기 작업을 한 `job`에 섞으면 전체 job이 더 높은 권한을 필요로 할 수 있습니다.

따라서 다음처럼 분리할 수 있습니다.

```yaml
jobs:
  test:
    permissions:
      contents: read

    runs-on: ubuntu-latest

    steps:
      - run: ./scripts/check.sh

  comment:
    needs: test

    permissions:
      contents: read
      pull-requests: write

    runs-on: ubuntu-latest

    steps:
      - run: ./scripts/post-result.sh
```

구조:

```text
신뢰하지 않는 코드 실행
→ 최소 읽기 권한

쓰기 작업
→ 필요한 job만 제한적으로 write
```

## 비밀값

API token, password, private key 같은 값을 workflow 파일에 직접 적지 않습니다.

피할 형태:

```yaml
env:
  API_TOKEN: abcdef123456
```

GitHub secret을 사용합니다.

```yaml
env:
  API_TOKEN: ${{ secrets.API_TOKEN }}
```

그러나 secret 저장소를 사용한다고 자동으로 안전해지는 것은 아닙니다.

### 확인할 사항

* secret을 로그에 출력하지 않는가?
* `set -x` 때문에 명령 인자가 로그에 노출되지 않는가?
* 전체 환경 변수를 출력하지 않는가?
* untrusted PR 코드가 secret을 읽을 수 있는 job에서 실행되지 않는가?
* 필요 없는 secret을 job에 전달하지 않는가?
* 운영 자격 증명을 단순 테스트에 사용하지 않는가?
* 노출이 의심되면 즉시 폐기·교체하는가?

### 로그 마스킹은 보조 수단이다

GitHub가 secret 값을 마스킹할 수 있지만:

```text
인코딩된 값

부분 문자열

변형된 값

프로그램에서 재구성한 값
```

까지 항상 완벽하게 가려진다고 가정하면 안 됩니다.

따라서 가장 안전한 방법은 애초에 불필요한 secret을 해당 실행 환경에 주지 않는 것입니다.

## fork Pull Request

외부 사용자가 repository를 fork한 뒤 Pull Request를 보낼 수 있습니다.

이때 PR 코드의 신뢰 수준은 다음과 같습니다.

```text
repository maintainer가 작성한 코드
≠
외부 contributor가 작성한 PR 코드
```

외부 PR 코드는 공격자가 의도적으로 작성한 코드일 수도 있다고 가정해야 합니다.

따라서 GitHub는 일반적으로 fork PR에서:

```text
repository secret

쓰기 가능한 token
```

사용을 제한합니다.

이 제한을 불편하다는 이유로 우회하지 않습니다.

### secret이 필요한 통합 테스트가 있다면

다음 방식을 검토합니다.

* 유지관리자가 승인한 별도 실행
* 최소 권한의 전용 테스트 계정
* 운영 시스템과 분리된 테스트 환경
* 짧은 수명의 임시 credential
* untrusted 코드를 직접 실행하지 않는 API 기반 검증
* manual approval gate

핵심 원칙:

```text
신뢰하지 않는 코드
+
운영 secret
+
쓰기 가능한 token
```

조합을 만들지 않습니다.

## `pull_request`와 `pull_request_target`

두 이벤트 이름은 비슷하지만 보안 모델이 크게 다릅니다.

## `pull_request`

일반적인 Pull Request 코드 검사에 사용합니다.

특징:

* PR의 변경 코드를 테스트하는 데 적합합니다.
* fork PR에서는 token 권한과 secret이 제한됩니다.
* 빌드·테스트처럼 untrusted code를 실행하는 CI에 적합합니다.

개념:

```text
PR 코드 실행
→ 낮은 권한
```

## `pull_request_target`

이 이벤트는 PR head가 아니라 **base 저장소의 기본 브랜치 쪽 workflow 정의를 기준으로 실행**되는 특성이 있습니다.

따라서 일반 `pull_request`보다 높은 권한이나 repository secret에 접근할 수 있는 상황이 생길 수 있습니다.

이 이벤트 자체가 위험한 것은 아닙니다.

위험한 것은 다음 조합입니다.

```text
pull_request_target
+
높은 권한 또는 secret
+
PR head 코드 checkout
+
그 코드를 실행
```

예:

```yaml
on:
  pull_request_target:

jobs:
  unsafe:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@COMMIT_SHA
        with:
          ref: ${{ github.event.pull_request.head.sha }}

      - run: ./scripts/from-pull-request.sh
```

외부 공격자는 PR에서:

```text
scripts/from-pull-request.sh
```

를 수정할 수 있습니다.

그런데 workflow가 높은 권한이나 secret을 가진 context에서 해당 코드를 실행하면:

```text
외부 PR 코드
→ 권한 있는 runner에서 실행
→ token/secret 탈취 또는 저장소 변경 가능
```

이라는 구조가 만들어질 수 있습니다.

### 적절한 사용 범위

`pull_request_target`은 대표적으로 다음처럼 PR 메타데이터만 다루는 작업에 사용할 수 있습니다.

```text
label 지정

PR 제목 검사

자동 댓글

triage

metadata 기반 정책 적용
```

중요한 조건:

```text
신뢰하지 않는 PR head 코드를 실행하지 않음
```

꼭 필요한 이유가 없다면 일반 빌드와 테스트에는 `pull_request`를 사용합니다.

## 외부 Action 고정

외부 Action 역시 runner에서 실행되는 코드입니다.

다음처럼 tag만 사용하면:

```yaml
uses: vendor/action@v1
```

`v1`이라는 ref가 나중에 다른 commit을 가리킬 가능성이 있습니다.

검토한 전체 commit SHA에 고정합니다.

```yaml
uses: vendor/action@0123456789abcdef0123456789abcdef01234567 # v1.2.3
```

그러나 SHA pinning만 확인해서는 부족합니다.

다음도 검토합니다.

* 공식 소유자 또는 신뢰할 수 있는 maintainer인가?
* Marketplace 등록만 믿고 있는 것은 아닌가?
* Action 코드가 어떤 명령을 실행하는가?
* 어떤 token과 secret을 읽는가?
* repository contents를 어디로 전송할 가능성이 있는가?
* `post` step에서 어떤 작업을 하는가?
* release note와 실제 코드가 일치하는가?
* 업데이트 PR에서 SHA와 release 내용을 함께 확인했는가?

Action은 단순한 설정 조각이 아니라 **CI runner에서 실행되는 공급망 의존성**입니다.

## checkout 인증 정보

`actions/checkout`은 기본 설정에 따라 workflow용 인증 정보를 Git 설정에 남길 수 있습니다.

단순 테스트 job에서는 이후 Git push가 필요하지 않습니다.

따라서:

```yaml
- uses: actions/checkout@COMMIT_SHA
  with:
    persist-credentials: false
```

처럼 설정할 수 있습니다.

목적:

```text
나중 step이 실수 또는 악의적으로
checkout이 설정한 token을 사용해 push할 경로를 줄임
```

실제 push가 필요한 job이 있다면 그 job을 별도로 분리하고:

```text
정확한 권한
정확한 branch
정확한 credential
```

을 명시하는 편이 안전합니다.

## 신뢰하지 않는 값을 셸 명령에 넣지 않기

다음은 외부 사용자가 제어할 수 있는 값입니다.

```text
Pull Request 제목
branch 이름
issue 제목
issue 본문
commit message
PR body
일부 workflow input
```

이 값을 expression으로 shell command 내부에 직접 삽입하지 않습니다.

피할 형태:

```yaml
- run: echo "${{ github.event.pull_request.title }}" | tool
```

안전성을 높인 형태:

```yaml
- name: Check title
  env:
    PR_TITLE: ${{ github.event.pull_request.title }}

  run: python scripts/check_title.py
```

프로그램에서는:

```python
import os

title = os.environ["PR_TITLE"]
```

처럼 데이터로 읽고 검증합니다.

핵심 차이:

```text
위험한 구조
외부 입력 → shell program text 일부

더 안전한 구조
외부 입력 → 환경 변수의 데이터
```

## 워크플로 변경 리뷰

`.github/workflows/` 아래 파일을 단순 설정 파일로 취급하지 않습니다.

워크플로는 다음을 바꿀 수 있습니다.

```text
어떤 이벤트에서 실행되는가

어떤 shell command를 실행하는가

어떤 외부 Action을 실행하는가

어떤 secret에 접근하는가

어떤 token 권한을 가지는가

어떤 artifact를 업로드하는가

원격 저장소에 무엇을 쓰는가
```

즉, 실행 가능한 코드에 가깝습니다.

리뷰할 때 확인합니다.

```text
[ ] 실행 이벤트 범위가 넓어졌는가?

[ ] pull_request_target이 새로 추가됐는가?

[ ] write 권한이 추가됐는가?

[ ] secret 전달 범위가 늘어났는가?

[ ] 새로운 외부 Action이 추가됐는가?

[ ] Action 소유자가 변경됐는가?

[ ] Action SHA가 변경됐는가?

[ ] untrusted code를 높은 권한으로 실행하지 않는가?

[ ] shell에 외부 입력을 직접 삽입하지 않는가?

[ ] artifact에 민감한 파일이 들어가지 않는가?

[ ] checkout credential이 불필요하게 유지되지 않는가?

[ ] 로컬에서 재현 가능한 검사 경로가 유지되는가?
```

가능하면:

```text
CODEOWNERS
ruleset
required reviewer
```

등으로 workflow 변경에 추가 검토를 요구할 수 있습니다.

## 동시 실행 제어와 오래된 결과

같은 PR에 여러 commit이 연속으로 push될 수 있습니다.

```text
HEAD=A
→ CI A 실행

HEAD=B
→ CI B 실행

HEAD=C
→ CI C 실행
```

병합 판단에 중요한 것은 최신 PR head `C`의 검사 결과입니다.

오래된 A 실행이 나중에 성공했다고 해서 C가 성공했다는 의미가 아닙니다.

`concurrency`로 오래된 실행을 자동 취소할 수 있습니다.

```yaml
concurrency:
  group: ci-${{ github.workflow }}-${{ github.event.pull_request.number || github.ref }}
  cancel-in-progress: true
```

병합 직전에는 UI의 초록색 표시만 보는 것이 아니라:

```text
이 check가 최신 head commit에 대한 것인가?
```

를 확인해야 합니다.

## 실제 Pull Request 실습

`exercises/github-actions-ci`를 별도 저장소 또는 연습 브랜치에 게시합니다.

```bash
cd exercises/github-actions-ci
./scripts/check.sh
```

다음 순서로 확인합니다.

1. 최신 `main`에서 작업 브랜치를 만듭니다.
2. `src/change_record.py` 또는 테스트를 작게 수정합니다.
3. 로컬에서 `./scripts/check.sh`를 실행합니다.
4. 검사 성공 뒤 커밋하고 push합니다.
5. Pull Request를 엽니다.
6. workflow가 어떤 이벤트로 실행됐는지 확인합니다.
7. matrix로 생성된 각 job을 확인합니다.
8. checkout된 ref와 실행 SHA를 확인합니다.
9. 테스트 기대값을 의도적으로 변경해 CI를 실패시킵니다.
10. 실패한 `job`과 `step`을 찾습니다.
11. 로그에서 실제 실패 명령과 첫 오류를 찾습니다.
12. 로컬에서 같은 명령으로 실패를 재현합니다.
13. 코드를 수정하고 다시 로컬 검증합니다.
14. push하여 새 workflow run을 확인합니다.
15. 최신 head commit의 CI가 통과했는지 확인합니다.
16. repository ruleset에서 해당 check를 required status check로 지정합니다.
17. 실패한 상태에서 실제로 merge가 차단되는지 확인합니다.

연습을 위해 만든 실패 commit은 최종 브랜치에 반드시 남길 필요는 없습니다.

하지만 다음은 설명할 수 있어야 합니다.

```text
왜 실패했는가?

어느 step이 실패했는가?

어떤 명령이 non-zero exit code를 반환했는가?

로컬에서 어떻게 재현했는가?

어떤 수정으로 해결했는가?

왜 새 실행이 최신 commit에 대한 결과라고 판단할 수 있는가?
```

## 완료 기준

* Pull Request workflow가 어떤 이벤트로 실행됐는지 확인합니다.
* workflow run이 검사한 commit/ref를 확인합니다.
* PR head 자체의 검사와 현재 base와 통합된 상태의 검사가 다를 수 있음을 설명합니다.
* workflow 실행과 required status check를 구분합니다.
* repository ruleset 또는 branch protection이 실제 병합 정책을 강제한다는 점을 설명합니다.
* `GITHUB_TOKEN`의 최소 권한 원칙을 설명합니다.
* 읽기 전용 CI와 쓰기 권한이 필요한 자동화 job을 분리할 수 있습니다.
* fork Pull Request에서 secret과 write token을 제한하는 이유를 설명합니다.
* `pull_request`와 `pull_request_target`의 보안 모델 차이를 설명합니다.
* `pull_request_target`에서 untrusted head 코드를 실행하면 위험한 이유를 설명합니다.
* 외부 Action을 전체 commit SHA로 고정하는 이유와 그 한계를 설명합니다.
* `persist-credentials: false`를 사용하는 목적을 설명합니다.
* 신뢰하지 않는 값을 shell command text에 직접 삽입하지 않는 이유를 설명합니다.
* `.github/workflows/` 변경을 실행 코드 수준의 보안 변경으로 리뷰합니다.
* 실패한 workflow에서 `job`, `step`, 실제 명령과 최초 오류까지 추적합니다.
* 로컬에서 같은 명령을 실행해 CI 실패를 재현할 수 있습니다.
* 병합 직전에 최신 PR head commit의 필수 상태 검사가 통과했는지 확인합니다.
