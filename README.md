# C와 POSIX 프로그래밍 가이드

이 브랜치는 C로 작성하는 실제 프로젝트에 들어가기 전에 필요한 공통 기반, 구현 중 찾아볼 POSIX 문서와 프로젝트 완료 뒤 개발 능력을 다시 확인할 exercise를 제공합니다.

모든 문서를 먼저 외운 뒤 개발을 시작하지 않습니다.

```text
Stable Core
→ Actual Project
→ 필요한 문서를 JIT로 확인
→ Project PASS
→ exercise를 가이드 없이 재구현
→ 실패한 주제만 Rewind
```

Exercise는 프로젝트 진입 조건이 아닙니다.

## 대상 프로젝트

대표 적용 대상은 다음과 같습니다.

- C 라이브러리와 문자열 처리
- 포맷 출력과 가변 인자
- 파일 디스크립터 기반 입력 처리
- 정렬·스택·큐를 사용하는 알고리즘 프로그램
- process, pipe와 signal을 사용하는 Unix 프로그램
- pthread 기반 동시성 프로그램

현재 프로젝트 모음에서는 `libft`, `ft_printf`, `get_next_line`, `push_swap`, `minitalk`, `philo`, `minishell`과 같은 C 프로젝트에 적용할 수 있습니다. 각 프로젝트의 요구사항과 허용 API는 실제 프로젝트 저장소를 기준으로 합니다.

## 저장소 구성

```text
.
├── README.md
├── docs/
│   ├── 00-roadmap.md
│   ├── 01-foundations/
│   ├── 02-c-language/
│   ├── 03-unix-programming/
│   └── 90-appendix/
└── exercises/
    ├── owned-string/
    ├── diagnostic-formatter/
    ├── record-stream/
    ├── signal-loop/
    ├── command-runner/
    ├── account-simulator/
    ├── int-vector/
    └── command-pipeline/
```

## Stable Core

다음 여덟 문서는 프로젝트 종류가 달라져도 C 프로그램 작성에 반복해서 사용합니다.

### 기본 개발 과정

- [`편집·컴파일·실행`](docs/01-foundations/01-edit-compile-run.md)
- [`값·분기·반복`](docs/01-foundations/02-values-branches-loops.md)
- [`함수·배열·문자열`](docs/01-foundations/03-functions-arrays-text.md)
- [`입력 오류와 디버깅`](docs/01-foundations/04-input-errors-debugging.md)

### C 프로그램 공통 기반

- [`프로그램 구성과 전처리`](docs/02-c-language/01-c-program-model.md)
- [`메모리·포인터·문자열`](docs/02-c-language/02-memory-pointers-strings.md)
- [`자료구조와 API 작성`](docs/02-c-language/03-data-structures-api-design.md)
- [`빌드·링크·테스트`](docs/02-c-language/04-build-link-test.md)

## 프로젝트 진입 기준

다음 작업을 수행할 수 있으면 실제 프로젝트를 시작합니다.

- 여러 `.c` 파일과 헤더를 컴파일하고 링크합니다.
- 배열과 포인터를 구분하고 접근 가능한 범위를 설명합니다.
- 동적 메모리를 누가 해제하는지 정합니다.
- 함수의 성공, 잘못된 입력과 환경 실패를 반환값으로 구분합니다.
- 실패 전에 public 상태를 바꾸지 않거나 실패 뒤 남는 상태를 명시합니다.
- `make`, 테스트와 sanitizer를 실행하고 첫 오류를 읽습니다.

가변 인자, process, signal과 thread를 미리 끝내려고 프로젝트 시작을 늦추지 않습니다.

## Actual Project에서 먼저 할 일

1. 요구사항, 금지 함수, 입력과 출력 조건을 읽습니다.
2. 빌드 명령과 실패하는 초기 검사를 확인합니다.
3. 저장할 상태와 자원 소유자를 적습니다.
4. 가장 작은 정상 동작 하나를 끝까지 구현합니다.
5. 잘못된 입력과 할당·system call 실패를 재현합니다.
6. 새 기능을 추가할 때 기존 테스트를 다시 실행합니다.

## JIT / Rewind 지도

| 구현하거나 조사할 내용 | 문서 |
|---|---|
| 가변 인자와 포맷 문자열 | [`가변 인자 포맷 API`](docs/02-c-language/05-variadic-format-api.md) |
| `read`, `write`, EOF와 부분 입출력 | [`POSIX I/O와 stream 상태`](docs/03-unix-programming/01-posix-io-streams.md) |
| `fork`, `exec`, fd와 pipe | [`process, fd와 pipe`](docs/03-unix-programming/02-process-fd-pipe.md) |
| signal과 비동기 사건 전달 | [`signal과 event`](docs/03-unix-programming/03-signals-events.md) |
| 명령 문자열 파싱과 실행 | [`shell parser와 executor`](docs/03-unix-programming/04-shell-parser-executor.md) |
| pthread, mutex, deadlock과 시간 | [`thread와 시간`](docs/03-unix-programming/05-threads-time.md) |
| debugger, Readline와 출력 검사 | [`docs/90-appendix/`](docs/90-appendix/) |

같은 문서는 구현 중에는 JIT 자료로, 프로젝트 완료 뒤 exercise 실패 원인을 찾을 때는 Rewind 자료로 사용합니다.

## Project PASS 기준

실제 프로젝트의 고유 요구사항이 우선입니다. 공통적으로 다음을 확인합니다.

- 깨끗한 clone에서 빌드합니다.
- 정상, 빈 입력, 경계값과 잘못된 입력을 검사합니다.
- 할당, 파일, process와 thread 자원을 정리합니다.
- 허용된 도구에서 memory error와 undefined behavior를 확인합니다.
- 종료 상태, `stdout`과 `stderr`를 요구사항에 맞게 구분합니다.
- 검증하지 않은 platform과 실패 주입 범위를 기록합니다.

## Competency Suite

프로젝트를 PASS하고 일정 시간이 지난 뒤 README와 공개 API만 보고 다음 프로젝트를 다시 구현합니다.

### 핵심 재확인 프로젝트

- [`owned-string`](exercises/owned-string/): 동적 메모리, 별칭 입력과 실패 뒤 상태 보존
- [`diagnostic-formatter`](exercises/diagnostic-formatter/): 가변 인자, 포맷 해석과 제한된 버퍼
- [`record-stream`](exercises/record-stream/): 부분 읽기, EOF와 호출 사이 입력 상태
- [`signal-loop`](exercises/signal-loop/): signal handler와 일반 코드 분리
- [`command-runner`](exercises/command-runner/): 문자열 파싱, 메모리 소유와 process 정리
- [`account-simulator`](exercises/account-simulator/): mutex 순서와 원자적인 상태 변경

### 약한 부분을 좁혀 보는 프로젝트

- [`int-vector`](exercises/int-vector/): 동적 배열 증가와 실패 처리
- [`command-pipeline`](exercises/command-pipeline/): 두 process와 fd 처리

## FAIL → Rewind

1. 실패 입력과 관찰 결과를 고정합니다.
2. 요구사항 또는 자신의 상태 모델이 잘못됐는지 먼저 확인합니다.
3. 원인을 설명하지 못하는 문서만 다시 읽습니다.
4. 수정 전 실패를 재현하는 테스트를 남깁니다.
5. 기존 전체 검사를 다시 실행합니다.

## 실행

```sh
cd exercises/owned-string
make
make test
make sanitize
```

지원 환경에서는 `account-simulator`의 ThreadSanitizer 검사도 실행할 수 있습니다.

## 완료 기준

- Stable Core를 바탕으로 실제 C 프로젝트 하나를 PASS합니다.
- 프로젝트 중 필요한 JIT 문서만 선택해 적용합니다.
- 선택한 핵심 exercise를 가이드와 기존 구현 없이 다시 구현합니다.
- 실패 뒤 상태, 자원 정리와 테스트가 보장하는 범위를 설명합니다.

## 범위 밖

GUI, 임베디드 하드웨어, kernel 개발, 네트워크 프로토콜 전체 구현, 분산 시스템과 C 원자 연산의 전체 memory model은 직접 다루지 않습니다. 필요한 도메인 지식은 실제 프로젝트와 해당 전문 가이드에서 학습합니다.
