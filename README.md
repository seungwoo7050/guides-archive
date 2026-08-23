# Python 개발 기반

이 브랜치는 Python으로 작은 프로그램을 설계하고 외부 입력을 검증하며, 테스트와 패키징까지 마무리하는 과정을 다룹니다. Python 문법을 빠르게 훑고 끝내는 과정도 아니고, Django·FastAPI·데이터 처리 라이브러리와 머신러닝 프레임워크를 모두 선행 학습하는 과정도 아닙니다.

```text
실행 방법과 입력 규칙을 정합니다.
→ 데이터를 명확한 값으로 변환합니다.
→ 계산과 파일 입출력을 분리합니다.
→ 오류와 경계값을 테스트합니다.
→ 설치해서 실행할 수 있는 프로젝트로 완성합니다.
→ 만들 제품에 맞는 프레임워크나 프로젝트로 이동합니다.
```

## 대상 독자와 환경

- 조건문, 반복문과 함수를 사용해 본 경험이 있으면 시작할 수 있습니다.
- Python 3.12 이상과 UTF-8 텍스트 환경을 사용합니다.
- 필수 과정은 운영체제에 종속된 외부 패키지를 요구하지 않습니다.

## 완료 후 갖춰야 할 능력

- 스크립트 실행과 `python -m` 실행을 구분합니다.
- 이름과 객체, 가변성과 불변성, `==`와 `is`를 구분합니다.
- 함수의 입력, 반환값과 실패 조건을 정합니다.
- 타입 힌트와 실행 시 입력 검증의 역할을 구분합니다.
- 반복자, 생성기와 컨텍스트 관리자로 데이터 처리와 자원 정리를 표현합니다.
- `pathlib`, CSV, JSON과 `argparse`로 작은 CLI를 작성합니다.
- 단위, 통합과 종단 간 테스트를 목적에 맞게 나눕니다.
- `pyproject.toml`, 모듈 진입점과 콘솔 스크립트를 포함한 프로젝트를 구성합니다.
- wheel 또는 직접 설치 뒤 같은 명령을 재현합니다.

## 저장소 구성

```text
.
├── README.md
├── docs/
│   ├── 00-roadmap.md
│   ├── 01-language-and-runtime/
│   ├── 02-automation/
│   └── 03-quality/
└── exercises/
    ├── data-report/
    └── command-checker/
```

## 정본 필수 과정

### 1. 언어와 실행 방식

- [실행 환경과 모듈](docs/01-language-and-runtime/01-runtime-and-environment.md)
- [객체와 컬렉션](docs/01-language-and-runtime/02-objects-and-collections.md)
- [함수, 예외 처리와 타입 검증](docs/01-language-and-runtime/03-functions-errors-and-types.md)
- [반복자, 생성기와 컨텍스트 관리자](docs/01-language-and-runtime/04-iterators-generators-and-context-managers.md)

### 2. 파일, 구조화된 데이터와 CLI

- [파일, 구조화된 데이터와 CLI](docs/02-automation/01-files-structured-data-and-cli.md)

### 3. 테스트와 프로젝트 구성

- [재현 가능한 테스트](docs/03-quality/01-testing.md)
- [프로젝트 구조, 패키징과 타입 검사](docs/03-quality/02-project-structure-packaging-and-typing.md)

## 필수 프로젝트

[`data-report`](exercises/data-report/)는 CSV 또는 JSON을 읽어 category별 합계와 전체 합계를 만드는 CLI 프로그램입니다.

- 패키지와 모듈 진입점
- 불변 `Record`와 `Report`
- CSV·JSON 필드 검증
- `Decimal` 기반 합산
- 입력 순서와 무관한 정렬
- text·JSON 출력
- 파일 저장과 종료 상태
- `unittest` 검증
- 콘솔 스크립트 설치

문서를 모두 읽은 뒤 구현을 시작하지 않습니다. 실행 환경, 객체, 함수와 프로젝트 구성을 읽으면 `data-report`의 package와 데이터 모델부터 만들고, 필요한 문서를 이어서 읽습니다.

## 선택 심화 — 시스템 자동화

외부 프로그램을 실행하거나 여러 작업을 동시에 처리해야 할 때만 사용합니다.

- [외부 프로세스와 수명 관리](docs/02-automation/02-subprocess-and-process-lifecycle.md)
- [동시 실행, 취소와 자원 제한](docs/02-automation/03-concurrency-and-cancellation.md)
- [CLI 검사기 설계](docs/03-quality/03-cli-test-runner.md)
- [`command-checker`](exercises/command-checker/)

`command-checker`는 timeout, 출력 상한, POSIX 프로세스 그룹 정리, 병렬 실행과 JSON·JUnit 보고서를 다룹니다.

## 프레임워크와 프로젝트로 이동하는 기준

Python에는 서로 다른 목적의 프레임워크와 라이브러리가 많습니다. 이 브랜치를 마친 뒤 모두 학습하지 않습니다. 만들 제품을 먼저 정하고 하나의 경로를 선택합니다.

### 웹 API

다음 기준을 만족하면 FastAPI 또는 Django 계열 프로젝트로 이동할 수 있습니다.

- 외부 JSON을 검증해 내부 값으로 변환합니다.
- 함수의 실패를 HTTP 오류와 분리할 준비가 되어 있습니다.
- package, 설정과 테스트를 실행할 수 있습니다.
- 데이터베이스와 인증을 프레임워크 마법으로 처리하지 않고 별도 상태로 검토합니다.

선택 기준은 다음과 같습니다.

- 작고 명시적인 HTTP API와 비동기 I/O가 중심이면 FastAPI 계열을 검토합니다.
- 관리자 화면, ORM, 인증과 다수의 기본 기능이 필요한 제품이면 Django 계열을 검토합니다.

둘을 모두 선행 학습하지 않습니다. 실제 프로젝트의 요구사항과 배포 환경으로 하나를 선택합니다.

### 데이터 처리·ETL

CSV·JSON 검증, iterator와 패키징을 완료한 뒤 실제 데이터 처리 프로젝트로 이동합니다. pandas, Polars, workflow 도구와 저장소는 데이터 크기, 지연 요구, 실행 환경과 팀 표준이 정해진 뒤 선택합니다.

### 자동화·CLI와 개발 도구

필수 과정 뒤 바로 실제 자동화 프로젝트로 이동할 수 있습니다. 외부 process, 병렬 실행과 취소가 필요하면 `command-checker` 심화를 JIT로 사용합니다.

### 머신러닝

배열·수치 계산, 데이터셋, 모델 훈련과 배포는 별도 머신러닝 과정이 필요합니다. Python 언어 가이드 완료를 머신러닝 완료로 보지 않습니다.

## 다른 개발 트랙에서 사용하는 방법

- 클라우드·보안·운영체제의 Python 실습을 실행하려면 필수 과정만으로 충분합니다.
- 게임 서버에서는 bot, 부하 도구, replay 분석과 운영 자동화에 사용할 수 있습니다.
- Python 자체가 제품의 주 언어라면 위 전이 경로 중 하나를 골라 실제 프로젝트로 이동합니다.

## 완료 기준

- `data-report`의 CSV와 JSON 입력이 같은 `Report`를 만듭니다.
- 잘못된 필드, 빈 category와 유효하지 않은 amount를 거부합니다.
- 합산에 `Decimal`을 사용하고 결과 순서가 항상 같습니다.
- 정상 결과와 오류를 각각 `stdout`, `stderr`로 분리합니다.
- 성공과 입력·파일 오류의 종료 상태를 구분합니다.
- 프로젝트 테스트를 통과하고 설치 뒤 콘솔 스크립트를 실행합니다.
- 다음 프로젝트의 목적에 맞는 프레임워크 또는 라이브러리를 하나 선택하고, 선택하지 않은 도구를 선행 조건으로 만들지 않습니다.

## 범위 밖

Django, FastAPI, 데이터 처리, 머신러닝과 GUI 프레임워크의 전체 사용법은 포함하지 않습니다. 이 브랜치는 해당 분야로 이동할 수 있는 Python 실행·타입·입력·테스트·패키징 기반에서 끝납니다.
