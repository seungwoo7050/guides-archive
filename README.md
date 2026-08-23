# C++ 개발 가이드

이 브랜치는 C++ 문법을 모두 익힌 뒤 개발을 시작하도록 요구하지 않습니다. 프로젝트 종류와 상관없이 반복해서 필요한 객체 수명, 값, 자원 관리와 오류 처리만 먼저 익히고, 네트워크·렌더링·파일 형식처럼 특정 문제에 필요한 내용은 실제 구현 중에 확인합니다.

```text
Stable Core
→ Actual Project
→ JIT Guide
→ Project PASS
→ Competency Suite without Guide
→ 실패한 부분만 Rewind
```

## 대상 프로젝트와 언어 프로필

### Modern C++

- 일반 애플리케이션
- CMake 기반 라이브러리와 도구
- 동시 작업 처리와 파일 시스템 프로그램
- 성능과 자원 수명을 직접 다루는 프로젝트

### C++98 시스템 프로젝트

- 객체 모델과 STL 연습
- POSIX socket과 event loop
- 제한된 표준의 HTTP server
- 기존 C++98 코드베이스 유지보수

현재 프로젝트 모음에서는 `cpp-foundation`, `ft_container`, `ft_irc`, `miniRT`와 같은 프로젝트에 적용할 수 있습니다. C++98 프로젝트라고 해서 Modern C++의 모든 기능을 흉내 내지 않습니다.

## 저장소 구성

```text
.
├── README.md
├── docs/
│   ├── 01-modern-cpp/
│   ├── 02-cpp98-systems/
│   └── 90-appendix/
└── exercises/
    ├── mini-vector/
    ├── command-service/
    ├── local-job-runner/
    └── line-server/
```

## Stable Core

### Modern C++ 공통 기반

다음 여섯 문서는 프로젝트 종류가 달라져도 목록을 늘리지 않습니다.

1. [`프로그램·빌드·CMake`](docs/01-modern-cpp/01-program-build-cmake.md)
2. [`값·수명·복사·이동`](docs/01-modern-cpp/02-values-lifetimes-and-move.md)
3. [`RAII·smart pointer·Rule of Zero`](docs/01-modern-cpp/03-raii-smart-pointers-and-rule-of-zero.md)
4. [`클래스·역할 분리·다형성`](docs/01-modern-cpp/04-classes-responsibilities-and-polymorphism.md)
5. [`오류·optional·variant·expected`](docs/01-modern-cpp/05-errors-optional-variant-and-expected.md)
6. [`algorithm·range·template·concept`](docs/01-modern-cpp/06-algorithms-ranges-templates-and-concepts.md)

### C++98 프로젝트에 추가할 기반

Modern C++의 개념을 먼저 이해한 뒤 다음 문서를 추가합니다.

1. [`Modern C++에서 C++98로 옮기기`](docs/90-appendix/01-modern-to-cpp98-crosswalk.md)
2. [`프로그램과 타입 모델`](docs/02-cpp98-systems/01-program-and-type-model.md)
3. [`수명·값·소유권`](docs/02-cpp98-systems/02-lifetime-value-and-ownership.md)
4. [`객체에 역할 나누기`](docs/02-cpp98-systems/03-assigning-object-responsibilities.md)
5. [`상속과 다형성`](docs/02-cpp98-systems/04-inheritance-and-polymorphism.md)
6. [`오류 처리·입력 검증·캐스트`](docs/02-cpp98-systems/05-errors-validation-and-casts.md)
7. [`template·iterator·STL`](docs/02-cpp98-systems/06-templates-iterators-and-stl.md)

## 프로젝트 진입 기준

### Modern C++

- target 단위로 CMake build를 구성합니다.
- 값, 참조, pointer와 객체 수명을 구분합니다.
- 소유 자원은 RAII 객체가 정리하도록 만듭니다.
- 복사와 이동 가능 여부를 의도적으로 정합니다.
- 오류가 호출자에게 전달되는 방법을 정합니다.
- 단위 테스트와 sanitizer 또는 동등한 검사를 실행합니다.

### C++98

위 개념을 C++98 제약에서 표현할 수 있어야 합니다.

- Rule of Three와 수동 소유권을 설명합니다.
- STL container와 iterator의 무효화 조건을 확인합니다.
- exception, 반환값과 종료 상태를 구분합니다.
- C++98 compiler와 build option에서 실제로 컴파일합니다.

## Actual Project에서 먼저 할 일

1. compiler standard, build target과 실행 파일을 확인합니다.
2. public API와 자원 소유자를 찾습니다.
3. 입력 하나가 상태를 바꾸고 출력되는 경로를 추적합니다.
4. 실패해도 유지해야 할 값과 반드시 정리할 자원을 적습니다.
5. 가장 작은 기능을 구현하고 전체 회귀 검사를 실행합니다.

## JIT / Rewind 지도

- [`동시 실행·시간·filesystem`](docs/01-modern-cpp/07-concurrency-time-and-filesystem.md)
- [`테스트·디버깅·도구`](docs/01-modern-cpp/08-testing-debugging-and-tooling.md)
- [`STL로 문제 풀기`](docs/02-cpp98-systems/07-solving-problems-with-stl.md)
- [`POSIX socket과 event loop`](docs/02-cpp98-systems/08-posix-sockets-and-event-loop.md)
- [`객체지향 HTTP server`](docs/02-cpp98-systems/09-object-oriented-http-server.md)
- [`compiler와 운영체제 차이`](docs/90-appendix/02-compiler-platform-notes.md)
- [`C++98 빌드와 호환성`](docs/90-appendix/03-cpp98-build-and-compatibility.md)
- [`STL 내부 동작`](docs/90-appendix/04-stl-internals.md)

프로젝트가 해당 문제에 도달하기 전에는 선행 과제로 만들지 않습니다.

## Project PASS 기준

- 실제 요구사항과 공개 API를 만족합니다.
- Debug와 필요한 Release build를 성공시킵니다.
- 정상, 경계, 잘못된 입력과 자원 실패를 검사합니다.
- 소유 자원이 성공·실패·취소·종료 경로에서 정리됩니다.
- 동시 실행이 있다면 `sleep`에 의존하지 않는 검사를 사용합니다.
- 네트워크 프로젝트는 부분 입출력, 연결 종료, backpressure와 반복 연결을 확인합니다.
- 지원하지 않거나 검사하지 않은 compiler와 platform을 명시합니다.

## Competency Suite

실제 프로젝트를 PASS하고 일정 시간이 지난 뒤 README와 공개 API만 보고 다시 구현합니다.

| 프로젝트 | 다시 확인하는 능력 |
|---|---|
| [`mini-vector`](exercises/mini-vector/) | raw storage, 객체 수명, template와 exception 뒤 복구 |
| [`command-service`](exercises/command-service/) | C++98 소유권, 역할 분리, 입력 검증과 다형성 |
| [`local-job-runner`](exercises/local-job-runner/) | queue, 취소, 동시 종료와 journal |
| [`line-server`](exercises/line-server/) | fd 수명, 부분 입출력, event loop와 backpressure |

### 허용하는 자료

- 언어와 표준 라이브러리 공식 문서
- compiler 오류 메시지
- 운영체제와 프로토콜 공식 문서

### 보지 않는 자료

- 해당 exercise의 구현
- 같은 문제를 그대로 풀이한 가이드
- 이전 자신의 구현

## FAIL → Rewind

실패한 입력을 고정하고 원인을 설명하지 못하는 문서만 다시 읽습니다. 수정 전 실패를 검출하는 테스트를 남기고 전체 검사를 다시 실행합니다.

## 완료 기준

- 선택한 언어 프로필의 Stable Core를 이해합니다.
- 실제 C++ 프로젝트 하나를 PASS합니다.
- 필요한 JIT 문서를 선택해 적용합니다.
- 하나 이상의 competency project를 가이드 없이 재구현합니다.
- 객체 수명, 실패 뒤 상태와 검증 범위를 설명합니다.

## 범위 밖

이 브랜치는 특정 제품의 업무 규칙, 네트워크 프로토콜 전체, 렌더링 수학, 파일 형식과 데이터베이스 설계를 미리 가르치지 않습니다. 해당 지식은 실제 프로젝트와 전문 가이드에서 학습합니다.
