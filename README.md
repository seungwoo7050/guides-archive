# Java 기초 개발 가이드

이 브랜치는 Java 프로그램을 직접 만들고 검증하는 데 필요한 언어·runtime·빌드·테스트 기반을 제공합니다. 최종 목적은 Java 문법을 끝없이 확장하는 것이 아니라, 명확한 기준을 통과한 뒤 [`backend-spring-boot`](https://github.com/seungwoo7050/guides-archive/tree/backend-spring-boot) 또는 다른 Java 프로젝트로 이동하는 것입니다.

```text
Java Stable Foundation
→ Spring Boot 진입 기준
→ 실제 Spring Boot 프로젝트
→ 필요할 때 Java 동시성·도구로 Rewind
```

Java 자체를 더 깊게 학습하려면 이 브랜치의 전체 통합 과정까지 이어서 수행할 수 있습니다.

## 대상 독자와 환경

- 조건문, 반복문, 함수와 배열 같은 일반 프로그래밍 개념을 알고 있으면 시작할 수 있습니다.
- Linux 또는 macOS
- JDK 17 이상
- Maven 3.9 이상

각 exercise는 독립된 Maven 프로젝트입니다.

```sh
mvn clean test
```

## Stable Language Foundation

### 1. 실행과 언어 기초

- [JDK·JVM과 첫 프로그램](docs/01-language-and-domain/01-jdk-jvm-and-first-program.md)
- [Java 언어 기초](docs/01-language-and-domain/02-java-language-foundations.md)
- [Number Report](exercises/number-report/README.md)

### 2. 빌드와 테스트

- [Maven Wrapper와 build lifecycle](docs/03-build-test-and-evidence/01-maven-wrapper-and-lifecycle.md)
- [JUnit·AssertJ와 test double](docs/03-build-test-and-evidence/02-junit-assertj-and-test-doubles.md)

### 3. 타입, 데이터와 실패

- [record, sealed type과 값 모델](docs/01-language-and-domain/03-domain-types-records-and-sealed-types.md)
- [collection, Stream과 숫자](docs/01-language-and-domain/04-collections-streams-and-numeric-invariants.md)
- [오류, 검증, 시간과 식별자](docs/01-language-and-domain/05-errors-validation-time-and-identifiers.md)

## Spring Boot 진입 기준

다음 작업을 수행할 수 있으면 Java 과정 전체를 먼저 끝내지 않고 `backend-spring-boot`로 이동할 수 있습니다.

- package가 있는 Java source를 Maven으로 build하고 test합니다.
- 기본형과 참조형, `null`, 값 동등성과 객체 동일성을 구분합니다.
- record, enum과 sealed type으로 허용할 상태를 제한합니다.
- 외부 입력을 생성 시점이나 명시적인 validator에서 거부합니다.
- collection의 순서, 중복과 key 조건에 맞는 구현을 선택합니다.
- 정수 overflow와 `BigDecimal` 반올림 규칙을 명시합니다.
- 입력 오류, 현재 상태에서의 거절과 실행 환경 실패를 구분합니다.
- JUnit으로 정상 결과, 실패 뒤 상태와 외부 효과를 검증합니다.
- `Clock`과 명시적인 ID를 주입해 test를 반복 실행합니다.

이 기준을 통과하면 Spring의 Application Context, 설정과 MVC 요청 처리를 학습합니다. thread pool, JFR과 고급 동시성을 모두 선행 조건으로 만들지 않습니다.

## 언어 기반 검증 프로젝트

### 필수 진입 검증

- [`number-report`](exercises/number-report/): 입력, 계산, `stdout`·`stderr`와 종료 상태

### 전체 Java 과정 검증

- [`counter-race`](exercises/counter-race/): lost update와 잠금
- [`bounded-task-runner`](exercises/bounded-task-runner/): 제한된 queue, 거절, 취소와 종료
- [`concurrent-job-ledger`](exercises/concurrent-job-ledger/): 값 타입, 정확한 계산, 시간, 중복 요청, 잠금과 executor 통합

## Spring 진입 뒤 JIT / Rewind

Spring 프로젝트에서 다음 문제가 생기면 Java 문서와 exercise로 돌아옵니다.

| 문제 | Rewind 대상 |
|---|---|
| 값 타입과 collection 선택이 불명확함 | 타입·collection 문서 |
| 시간과 ID 때문에 test가 불안정함 | 오류·시간·식별자 문서 |
| 동시에 상태가 바뀜 | [동시성·잠금과 executor](docs/02-runtime-and-concurrency/01-concurrency-locking-and-executors.md) |
| 작업 queue 포화·취소·종료 | `bounded-task-runner` |
| build artifact 연결 문제 | Maven 문서와 `maven-artifact-boundary` |
| thread dump와 profiling 근거 필요 | 품질·profiling 선택 문서 |

## 선택 자료

- [품질 검사·profiling과 검증 근거](docs/03-build-test-and-evidence/03-quality-profiling-and-evidence.md)
- [`maven-artifact-boundary`](exercises/maven-artifact-boundary/)

## Java 전체 과정 완료 기준

Spring 진입 기준과 별도로 Java 자체 과정을 완료하려면 다음을 모두 만족합니다.

1. 필수 문서의 선택 이유를 설명합니다.
2. `number-report`, `counter-race`, `bounded-task-runner`와 `concurrent-job-ledger`의 테스트를 통과합니다.
3. 실패 사례가 기존 상태와 자원을 어떻게 남기는지 설명합니다.
4. 중복 제출, queue 포화, 잔액 부족, overflow와 종료를 결정적으로 재현합니다.
5. 각 프로젝트를 독립 디렉터리에서 build하고 실행합니다.

## 다음 단계

### Spring Boot 백엔드

가장 직접적인 후속 경로입니다.

```text
Java Stable Foundation
→ backend-spring-boot Stable Core
→ Actual Backend Project
```

### 다른 Java 프레임워크와 프로젝트

Android, desktop, batch, data processing과 game server는 서로 다른 runtime과 framework를 사용합니다. Java 완료 뒤 모든 프레임워크를 공부하지 않고 실제 제품과 팀의 stack을 기준으로 하나를 선택합니다.

## 범위 밖

Spring Boot, Android, ORM, web server와 game server framework의 전체 사용법은 포함하지 않습니다. 이 브랜치는 해당 과정에 진입할 Java 실행·타입·실패·빌드·테스트 기반을 제공합니다.
