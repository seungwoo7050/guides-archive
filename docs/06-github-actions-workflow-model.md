# GitHub Actions 워크플로 실행 모델 

## 목표

GitHub Actions YAML을 복사해 붙이는 데서 끝내지 않습니다. 다음 실행 구조를 설명할 수 있어야 합니다.

```text
이벤트
→ 워크플로 실행
→ job
→ runner
→ step
→ 명령 또는 Action
→ 종료 상태
→ 검사 결과
```

핵심 질문은 다음과 같습니다.

* 어떤 이벤트가 워크플로를 시작했는가?
* 어떤 `job`이 생성됐는가?
* 각 `job`은 어떤 runner에서 실행됐는가?
* 각 `step`은 셸 명령을 실행했는가, 외부 Action을 실행했는가?
* 실제 실패한 명령은 무엇인가?
* 실패가 코드 문제인지, 환경·권한·워크플로 문제인지 구분할 수 있는가?

## 워크플로 파일 위치

GitHub는 기본적으로 다음 경로의 YAML 파일을 워크플로로 읽습니다.

```text
.github/workflows/*.yml
.github/workflows/*.yaml
```

예:

```text
.github/workflows/ci.yml
.github/workflows/lint.yml
.github/workflows/release.yml
```

파일 이름 자체에 특별한 의미는 없습니다.

다만 다음처럼 역할이 드러나게 이름을 정하는 편이 좋습니다.

```text
ci.yml
→ 빌드와 테스트

lint.yml
→ 정적 검사와 포맷 검사

release.yml
→ 릴리스 또는 배포
```

이 과정에서는 빌드와 테스트를 담당하는 `ci.yml` 하나만 사용합니다.

## 이벤트와 워크플로 실행

워크플로의 `on`은 **어떤 GitHub 이벤트가 발생했을 때 새 workflow run을 만들지** 정의합니다.

```yaml
on:
  pull_request:

  push:
    branches:
      - main

  workflow_dispatch:
```

의미:

```text
pull_request
→ Pull Request 관련 이벤트에서 실행

push
→ 여기서는 main에 push가 발생할 때 실행

workflow_dispatch
→ 사용자가 GitHub Actions 화면이나 API에서 수동 실행 가능
```

### `pull_request`는 단순히 PR 생성 때만 실행되지 않는다

기본 `pull_request` 이벤트는 PR 생성뿐 아니라 대표적으로 다음 상황에서도 실행될 수 있습니다.

```text
PR 생성
새 커밋 push로 PR 갱신
PR 다시 열기
```

정확히 어떤 activity type을 받을지는 GitHub Actions 이벤트 설정에 따라 달라질 수 있습니다.

필요하다면 다음처럼 범위를 명시할 수 있습니다.

```yaml
on:
  pull_request:
    types:
      - opened
      - synchronize
      - reopened
```

### 같은 워크플로라도 이벤트에 따라 실행 문맥이 다르다

다음 두 실행은 같은 `ci.yml`을 사용하더라도 완전히 같은 조건이라고 볼 수 없습니다.

```text
pull_request 실행

push 실행
```

이벤트마다 다음 값이 달라질 수 있습니다.

```text
github.ref
github.sha
checkout 대상
이벤트 payload
GITHUB_TOKEN 권한
secrets 사용 가능 여부
```

따라서 "`CI에서는 성공했다`"라고만 말하지 않고 어떤 이벤트의 실행이었는지 확인해야 합니다.

## `job`

워크플로의 `jobs` 아래에 하나 이상의 `job`을 정의합니다.

```yaml
jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - run: ./scripts/check.sh
```

여기서:

```text
test
→ job 식별자

runs-on
→ 이 job이 실행될 runner 종류

steps
→ runner 안에서 순서대로 수행할 작업
```

### `job`은 기본적으로 독립적이다

다음과 같이 두 `job`이 있다고 가정합니다.

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - run: ./scripts/test.sh

  lint:
    runs-on: ubuntu-latest
    steps:
      - run: ./scripts/lint.sh
```

기본적으로 `test`와 `lint`는 서로의 완료를 기다릴 필요가 없습니다.

개념적으로:

```text
workflow run
├─ test job
│  └─ runner A
│
└─ lint job
   └─ runner B
```

둘은 가능한 경우 병렬로 실행될 수 있습니다.

### 실행 순서를 만들려면 `needs`

`package`가 `test` 성공 뒤에만 실행되어야 한다면:

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - run: ./scripts/check.sh

  package:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - run: ./scripts/package.sh
```

실행 관계:

```text
test
↓ 성공
package
```

여러 선행 `job`이 모두 필요한 경우:

```yaml
needs:
  - test
  - lint
```

처럼 지정할 수 있습니다.

### 언제 `job`을 나눌 것인가

검사 명령 하나를 이유 없이 여러 `job`으로 쪼개지 않습니다.

나눌 가치가 있는 경우:

```text
서로 다른 OS에서 실행해야 함

독립적으로 병렬 실행할 가치가 있음

실패 원인을 분리해서 보고 싶음

권한이 서로 다름

후속 job이 특정 결과물에만 의존함
```

반대로 하나의 `job` 안에서 순서대로 실행해야 하는 검사라면 여러 `step`으로 구성하는 편이 더 단순할 수 있습니다.

## runner

`runs-on`은 `job`이 실행될 환경을 선택합니다.

```yaml
runs-on: ubuntu-latest
```

대표적인 GitHub-hosted runner:

```text
ubuntu-latest
windows-latest
macos-latest
```

### runner는 일반적으로 매 job마다 새 환경이다

GitHub-hosted runner에서는 각 `job`이 기본적으로 새 가상 환경에서 시작합니다.

즉:

```text
job A에서 설치한 패키지
job A에서 만든 파일
job A에서 설정한 환경 변수
```

가 별도 `job B`에 자동으로 남는다고 가정하면 안 됩니다.

예:

```text
test job
→ runner A
→ build/output.zip 생성

package job
→ runner B
→ output.zip 자동 존재하지 않음
```

다른 `job`으로 파일을 전달해야 한다면 artifact 같은 명시적인 전달 방법이 필요합니다.

### 저장소 파일도 먼저 checkout해야 한다

runner가 생성됐다고 현재 GitHub 저장소 파일이 자동으로 작업 디렉터리에 준비되는 것은 아닙니다.

일반적으로 다음 Action을 사용합니다.

```yaml
- name: Checkout repository
  uses: actions/checkout@COMMIT_SHA
```

이후에야 저장소 내부의:

```text
src/
tests/
scripts/
```

등을 사용할 수 있습니다.

## `step`: `uses`와 `run`

`job`의 실제 작업은 `steps`에 정의합니다.

대표적인 두 종류가 있습니다.

```text
uses
run
```

## Action 실행: `uses`

```yaml
- name: Checkout repository
  uses: actions/checkout@COMMIT_SHA
```

`uses`는 이미 만들어진 Action을 실행합니다.

대상은 대표적으로 다음일 수 있습니다.

```text
GitHub 공식 Action
외부 저장소의 Action
현재 저장소 내부의 local Action
```

예:

```yaml
uses: actions/checkout@...
uses: actions/setup-python@...
```

## 셸 명령 실행: `run`

```yaml
- name: Run project checks
  run: ./scripts/check.sh
```

`run`은 runner의 셸에서 명령을 실행합니다.

개념적으로:

```text
runner 생성
→ 저장소 checkout
→ shell에서 ./scripts/check.sh 실행
→ 프로세스 종료 코드 확인
```

일반적인 Unix 명령 규약에서는:

```text
exit code 0
→ 성공

0이 아닌 exit code
→ 실패
```

입니다.

따라서:

```bash
./scripts/check.sh
```

가 `1`을 반환하면 기본적으로 해당 `step`이 실패합니다.

그리고 별도 예외 설정이 없다면:

```text
step 실패
→ job 실패
→ workflow run의 검사 결과에도 실패 반영
```

으로 이어집니다.

## checkout과 실행 환경 설정

runner에는 필요한 실행 환경을 명시적으로 구성하는 것이 좋습니다.

### 저장소 checkout

```yaml
- name: Checkout repository
  uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
  with:
    persist-credentials: false
```

`actions/checkout`은 workflow가 실행 중인 저장소 내용을 runner에 checkout합니다.

`persist-credentials: false`는 이후 step에서 checkout이 설정한 기본 Git 인증 정보를 그대로 사용하는 것을 막는 데 도움이 됩니다.

단순 테스트 job처럼 push가 필요 없는 경우 불필요한 쓰기 경로를 줄일 수 있습니다.

### Python 버전 설정

```yaml
- name: Set up Python
  uses: actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97 # v7.0.0
  with:
    python-version: '3.13'
```

runner 이미지에 Python이 이미 설치되어 있을 수 있지만 그것만 믿지 않습니다.

이유:

```text
runner 이미지가 갱신될 수 있음

기본 Python 버전이 달라질 수 있음

프로젝트가 지원하는 정확한 버전을 검증해야 함
```

따라서 지원 런타임을 검증하는 CI에서는 버전을 명시하는 편이 재현성이 높습니다.

## 외부 Action을 SHA로 고정하는 이유

다음처럼 tag를 사용할 수도 있습니다.

```yaml
uses: vendor/action@v1
```

하지만 tag는 저장소 관리자가 다른 commit을 가리키게 변경할 수 있는 Git ref입니다.

따라서 실행 대상을 정확히 고정하려면 전체 commit SHA를 사용할 수 있습니다.

```yaml
uses: vendor/action@0123456789abcdef0123456789abcdef01234567 # v1.2.3
```

여기서 실제 실행 대상을 결정하는 것은:

```text
0123456789abcdef...
```

입니다.

뒤의:

```text
# v1.2.3
```

은 사람이 읽기 위한 주석일 뿐입니다.

이 방식의 목적은:

```text
검토한 코드
=
실제 CI에서 실행되는 코드
```

관계를 더 명확하게 만드는 것입니다.

다만 SHA 고정만으로 해당 Action이 안전하다는 의미는 아닙니다.

별도로 소유자, 코드, 권한과 공급망 위험을 검토해야 합니다.

## 로컬과 CI가 같은 명령을 사용해야 하는 이유

CI YAML에 실제 검사 논리를 길게 작성하면 로컬 검사와 CI 검사가 점차 달라지기 쉽습니다.

예:

```yaml
- run: python -m compileall src
- run: python -m unittest discover -s tests
- run: python scripts/check_schema.py
- run: python scripts/check_format.py
```

개발자는 로컬에서 다른 명령을 실행할 수 있습니다.

```text
로컬
→ 일부 테스트만 실행

CI
→ 추가 검사 실행
```

그러면 다음 상황이 생깁니다.

```text
"내 컴퓨터에서는 성공했는데 CI에서 실패한다"
```

프로젝트 검사 진입점을 하나로 통일하면 차이를 줄일 수 있습니다.

```yaml
- run: ./scripts/check.sh
```

개발자도 동일하게 실행합니다.

```bash
./scripts/check.sh
```

구조:

```text
개발자 로컬
        \
         → scripts/check.sh → 실제 검사들
        /
GitHub Actions
```

검사 순서나 내용을 변경할 때 `scripts/check.sh`를 수정하면 양쪽이 같이 바뀝니다.

물론 CI에서만 가능한 별도 검사가 있을 수 있으므로 모든 검사를 반드시 완전히 동일하게 만들 수 있다는 뜻은 아닙니다.

핵심은 **공유 가능한 검사 논리는 한 곳에 두는 것**입니다.

## matrix

같은 `job`을 여러 환경 조합에서 반복 실행하려면 matrix를 사용할 수 있습니다.

예:

```yaml
strategy:
  fail-fast: false

  matrix:
    python-version:
      - '3.11'
      - '3.13'
```

step에서 현재 조합의 값을 사용합니다.

```yaml
- uses: actions/setup-python@COMMIT_SHA
  with:
    python-version: ${{ matrix.python-version }}
```

이 경우 개념적으로 다음 두 job instance가 만들어집니다.

```text
test (Python 3.11)

test (Python 3.13)
```

### `fail-fast: false`

matrix job 중 하나가 실패해도 다른 조합을 계속 실행합니다.

예:

```text
Python 3.11 → 성공
Python 3.13 → 실패
Python 3.14 → 계속 실행
```

지원 버전 전체의 상태를 한 번에 확인하고 싶을 때 유용합니다.

반대로 빠른 실패가 더 중요하다면 기본 동작을 유지할 수 있습니다.

### matrix를 과도하게 늘리지 않는다

예:

```text
Python 4종
× OS 3종
× DB 3종
= 36개 실행
```

실제 지원 범위가 아닌 조합까지 모두 넣으면 CI 시간과 비용만 증가할 수 있습니다.

matrix에는 다음을 기준으로 넣습니다.

```text
실제 공식 지원 버전인가?

호환성 차이가 발생할 가능성이 있는가?

사용자가 실제로 사용하는 환경인가?

추가 실행 비용만큼 검증 가치가 있는가?
```

## context와 expression

`${{ ... }}`는 GitHub Actions가 workflow를 평가하면서 값을 가져오는 expression 문법입니다.

예:

```yaml
${{ github.ref }}
${{ matrix.python-version }}
${{ secrets.DEPLOY_TOKEN }}
```

대표적인 context:

```text
github
→ 이벤트, 저장소, ref, actor, event payload 등

matrix
→ 현재 matrix 조합

runner
→ runner OS와 여러 실행 환경 정보

env
→ 현재 scope의 환경 변수

secrets
→ GitHub에 등록된 secret

needs
→ 의존하는 job의 결과와 output
```

### expression과 shell은 다른 평가 단계다

다음 코드를 보면:

```yaml
run: echo "${{ github.ref }}"
```

개념적으로는 먼저 GitHub Actions가:

```text
${{ github.ref }}
```

를 실제 값으로 치환하고, 그 결과를 runner의 shell에 전달합니다.

즉:

```text
GitHub Actions expression 처리
→ shell 명령 실행
```

두 단계가 존재합니다.

이 구분은 보안상 중요합니다.

## 신뢰하지 않는 값을 셸 명령에 직접 넣지 않기

Pull Request 제목처럼 외부 사용자가 제어할 수 있는 값을 다음처럼 직접 `run` 문자열에 삽입하지 않습니다.

```yaml
- run: echo "${{ github.event.pull_request.title }}" | tool
```

문제가 되는 이유는 값이 GitHub expression 단계에서 문자열 안에 삽입된 뒤 shell에 전달되기 때문입니다.

특수문자가 예상하지 못한 shell 문법으로 해석될 위험이 생깁니다.

대신 환경 변수로 전달합니다.

```yaml
- name: Check title
  env:
    PR_TITLE: ${{ github.event.pull_request.title }}
  run: python scripts/check_title.py
```

프로그램에서는:

```text
환경 변수 값으로 읽기
→ 길이 검증
→ 허용 문자 검증
→ 업무 규칙 검증
```

처럼 처리합니다.

환경 변수 사용이 모든 공격을 자동으로 차단한다는 뜻은 아닙니다.

핵심은 **신뢰하지 않는 데이터를 shell 프로그램 텍스트 자체로 만들지 않는 것**입니다.

## 권한

GitHub Actions는 workflow에서 `GITHUB_TOKEN` 권한을 지정할 수 있습니다.

읽기 전용 CI 예:

```yaml
permissions:
  contents: read
```

저장소를 checkout하고 테스트만 실행하는 경우 일반적으로 저장소 내용을 읽을 수 있으면 충분합니다.

불필요한:

```text
contents: write
issues: write
pull-requests: write
packages: write
```

권한까지 줄 이유가 없습니다.

### 모든 권한을 먼저 비우기

```yaml
permissions: {}
```

로 시작한 뒤 필요한 `job`에 필요한 권한만 줄 수도 있습니다.

예:

```yaml
jobs:
  test:
    permissions:
      contents: read

  comment:
    permissions:
      contents: read
      pull-requests: write
```

구조:

```text
test job
→ 코드 읽기와 테스트만 수행
→ read 권한

comment job
→ PR에 댓글 작성 필요
→ pull-requests: write 추가
```

이것이 최소 권한 원칙입니다.

권한 부족으로 CI가 실패했다고 곧바로:

```yaml
permissions: write-all
```

을 추가하지 않습니다.

먼저 어떤 API 작업이 어떤 권한을 요구하는지 확인합니다.

## 중복 실행 취소

같은 PR에 짧은 시간 동안 여러 번 push하면 오래된 커밋의 CI가 계속 실행될 수 있습니다.

예:

```text
commit A push
→ CI A 실행 중

commit B push
→ CI B 실행

commit C push
→ CI C 실행
```

A와 B의 결과는 이미 최신 상태를 대표하지 않습니다.

`concurrency`로 이전 실행을 취소할 수 있습니다.

```yaml
concurrency:
  group: ci-${{ github.workflow }}-${{ github.event.pull_request.number || github.ref }}
  cancel-in-progress: true
```

의도:

```text
같은 workflow
+
같은 PR 또는 ref
→ 같은 concurrency group
```

새 실행이 시작되면 같은 group의 이전 진행 중 실행을 취소합니다.

다른 PR은 PR 번호가 다르므로 서로 다른 group을 사용할 수 있습니다.

이 기능은 계산 자원 낭비를 줄이는 것뿐 아니라 **오래된 CI 결과를 최신 결과와 혼동하는 문제**도 줄입니다.

## 실패 위치 찾기

CI 실패를 볼 때 마지막 빨간 줄만 읽지 않습니다.

다음 순서로 좁힙니다.

```text
workflow run
→ 실패한 job
→ 실패한 step
→ step이 실행한 실제 명령
→ 처음 나타난 의미 있는 오류
→ 종료 코드
```

예:

```text
Install dependencies
→ 실패

Run tests
→ skipped
```

이 경우 테스트가 실패한 것이 아닙니다.

실제 원인은 dependency 설치입니다.

또는:

```text
Run tests
→ 여러 테스트 출력
→ 마지막 줄: process exited with code 1
```

에서 마지막 줄은 원인이 아니라 결과일 뿐입니다.

실제 원인은 그 앞의:

```text
AssertionError
ModuleNotFoundError
permission denied
syntax error
```

등일 수 있습니다.

### 로컬에서 동일 명령 재현

CI가 다음을 실행했다면:

```bash
./scripts/check.sh
```

로컬에서도 먼저 같은 명령을 실행합니다.

```bash
./scripts/check.sh
```

같이 실패한다면 코드나 테스트 자체 문제일 가능성이 높습니다.

로컬에서는 성공하고 CI에서만 실패한다면 환경 차이를 조사합니다.

대표적인 차이:

* Python 또는 Node.js 버전
* runner OS
* CPU 아키텍처
* 환경 변수
* locale
* timezone
* 파일 이름 대소문자 처리
* 실행 권한
* checkout 깊이
* Git 이력 존재 여부
* secret 유무
* `GITHUB_TOKEN` 권한
* 네트워크 접근 가능 여부
* 설치된 시스템 패키지
* 캐시 유무

## `cache`와 `artifact`

둘은 이름이 비슷한 저장 기능처럼 보이지만 목적이 다릅니다.

### cache

목적:

```text
다음 workflow run에서도 재사용하여
설치나 빌드 시간을 줄임
```

대표 대상:

```text
패키지 관리자 다운로드 캐시
컴파일 캐시
일부 의존성 캐시
```

중요한 원칙:

```text
cache hit
→ 빠름

cache miss
→ 느리더라도 정상 동작해야 함
```

즉, cache 존재가 correctness의 전제 조건이 되어서는 안 됩니다.

### artifact

목적:

```text
현재 workflow run에서 생성한 결과물을 보관
```

대표 예:

```text
빌드 바이너리
테스트 리포트
coverage 결과
로그
패키징 결과
```

또한 서로 다른 `job` 사이에서 생성물을 전달하는 데 사용할 수 있습니다.

개념적으로:

```text
build job
→ artifact upload

test/package job
→ artifact download
```

정리하면:

```text
cache
→ 성능 최적화용 재사용 데이터

artifact
→ 실행 결과물 보관·전달
```

이 실습 프로젝트에는 외부 의존성이 없으므로 둘 다 사용하지 않습니다.

## `github-actions-ci` 워크플로 읽기

```bash
cd exercises/github-actions-ci

sed -n '1,240p' .github/workflows/ci.yml

./scripts/check.sh
```

다음을 찾아 직접 설명합니다.

* workflow를 시작하는 이벤트
* `contents: read`
* 중복 실행을 제어하는 `concurrency`
* Python matrix
* `fail-fast`
* `actions/checkout` SHA 고정
* `actions/setup-python` SHA 고정
* 로컬과 CI가 공유하는 `./scripts/check.sh`
* 각 `job`이 사용하는 runner
* 각 `step`이 `uses`인지 `run`인지

## 완료 기준

* 이벤트, workflow run, `job`, runner와 `step`의 관계를 설명합니다.
* `uses`와 `run`의 실행 모델 차이를 설명합니다.
* 한 `job`과 다른 `job`이 기본적으로 별도 runner에서 실행됨을 설명합니다.
* 0이 아닌 종료 코드가 `step`과 `job` 실패로 연결되는 기본 흐름을 설명합니다.
* 로컬과 CI에서 같은 프로젝트 검사 진입점을 사용할 수 있습니다.
* matrix를 실제 지원 범위에 맞게 구성합니다.
* `fail-fast: false`가 어떤 결과 수집 방식에 적합한지 설명합니다.
* 외부 Action의 tag와 SHA 고정 방식 차이를 설명합니다.
* workflow가 요청하는 `GITHUB_TOKEN` 권한을 설명합니다.
* 실패한 workflow에서 실제 실패 명령까지 추적할 수 있습니다.