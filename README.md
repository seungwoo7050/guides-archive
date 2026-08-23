# Spring Boot 백엔드 개발 가이드

이 브랜치는 Java, HTTP와 SQL의 기본기를 익힌 개발자가 실제 Spring Boot 프로젝트에 들어가기 위한 최소 실행 원리, 기능별 JIT 문서와 프로젝트 완료 뒤 역량 검증을 제공합니다.

```text
Java Stable Foundation
→ Spring Boot Stable Core
→ Actual Backend Project
→ JIT Guide
→ Project PASS
→ Competency Suite
→ 실패한 부분만 Rewind
```

이 저장소 자체가 최종 프로젝트를 대신하지 않습니다.

## 선행 지식

[`java`](https://github.com/seungwoo7050/guides-archive/tree/java)의 Spring Boot 진입 기준을 만족하거나 다음 작업을 수행할 수 있어야 합니다.

- Maven으로 Java 프로젝트를 build하고 test합니다.
- record, enum, collection과 명시적인 오류 타입을 사용합니다.
- 외부 입력을 runtime에서 검증합니다.
- `Clock`과 ID를 주입해 재현 가능한 test를 작성합니다.
- HTTP method, status, header와 JSON body를 구분합니다.
- 기본 SQL과 transaction의 목적을 설명합니다.

## Stable Core

프로젝트에 들어가기 전에 다음 세 문서를 읽습니다.

1. [`Application Context와 Bean 수명`](docs/01-spring-core/01-application-context-and-lifecycle.md)
2. [`설정, profile과 readiness`](docs/01-spring-core/02-configuration-profiles-and-readiness.md)
3. [`Spring MVC 검증과 ProblemDetail`](docs/02-web-and-security/01-mvc-validation-and-problem-detail.md)

인증, 데이터베이스, Redis와 Kafka는 모든 프로젝트에 필요한 것이 아니므로 Stable Core에 포함하지 않습니다.

## 프로젝트 진입 기준

- Spring이 객체를 만드는 시점과 application code가 직접 만드는 객체를 구분합니다.
- 설정 누락을 port를 열기 전에 거부합니다.
- application 생성과 실제 network listen을 분리합니다.
- request body를 검증한 뒤 내부 타입으로 변환합니다.
- 입력 오류, 업무 거절과 예기치 않은 실패를 다른 HTTP 응답으로 변환합니다.
- 최소한의 context test와 web test를 실행합니다.

## Actual Project에서 먼저 할 일

1. JDK, Maven Wrapper, profile과 실행 명령을 확인합니다.
2. request 하나가 controller, service, repository와 response를 거치는 경로를 추적합니다.
3. 설정을 읽는 위치와 startup validation을 확인합니다.
4. transaction을 시작하고 끝내는 위치를 확인합니다.
5. 가장 작은 endpoint를 정상·검증 실패·업무 거절까지 구현합니다.
6. 실제 database나 외부 service가 필요한 검사를 분리합니다.

## JIT / Rewind 지도

| 구현할 내용 | 문서 |
|---|---|
| 인증과 요청 권한 | [`Spring Security 요청 모델`](docs/02-web-and-security/02-spring-security-request-model.md) |
| 객체 소유권과 CSRF | [`인증, 객체 권한과 CSRF`](docs/02-web-and-security/03-authentication-authorization-and-csrf.md) |
| JPA transaction과 동시성 | [`JPA transaction과 잠금`](docs/03-persistence-and-cache/01-jpa-transactions-and-locking.md) |
| schema 변경 | [`Flyway와 schema 연결`](docs/03-persistence-and-cache/02-flyway-and-schema-integration.md) |
| Redis cache와 임시 상태 | [`Spring Data Redis`](docs/03-persistence-and-cache/03-spring-data-redis.md) |
| Kafka와 Avro | [`Spring Kafka와 Avro`](docs/04-distributed-adapters/01-spring-kafka-and-avro.md) |
| Outbox와 예약 실행 | [`Outbox와 Spring scheduling`](docs/04-distributed-adapters/02-outbox-and-scheduling.md) |
| 외부 HTTP와 Circuit Breaker | [`Resilience4j HTTP client`](docs/04-distributed-adapters/03-resilience4j-http-clients.md) |
| test 범위 선택 | [`Testcontainers와 WireMock`](docs/05-quality-and-operations/01-test-boundaries-testcontainers-and-wiremock.md) |
| health, metric, log와 trace | [`Actuator와 관측`](docs/05-quality-and-operations/02-actuator-metrics-logging-and-tracing.md) |

## Project PASS 기준

- 깨끗한 환경에서 build와 test를 통과합니다.
- 필수 설정이 없으면 port를 열기 전에 실패합니다.
- 정상, 검증 실패, 권한 거절, 업무 거절과 예기치 않은 오류 응답을 구분합니다.
- schema migration이 새 DB와 기존 DB에서 재현됩니다.
- transaction과 database 제약으로 동시에 바뀌는 값을 보호합니다.
- 사용한 외부 service의 timeout, 오류 분류와 제한된 재시도를 검사합니다.
- 필요한 통합 test가 실제 PostgreSQL, Redis, Kafka 또는 HTTP server를 사용합니다.
- health와 readiness가 실제 준비 상태를 반영합니다.
- 사용하지 않은 Redis·Kafka 기능을 프로젝트 완료 조건으로 추가하지 않습니다.

## Competency Suite

실제 프로젝트가 PASS한 뒤 가이드를 먼저 다시 읽지 않고 다음 프로젝트를 구현합니다.

| 필수 프로젝트 | 확인하는 능력 |
|---|---|
| [`request-preview-api`](exercises/request-preview-api/) | 설정, request, 업무 규칙과 오류 응답 |
| [`project-access-api`](exercises/project-access-api/) | 인증, 요청 권한, 객체 소유권과 CSRF |
| [`inventory-reservation`](exercises/inventory-reservation/) | JPA transaction, row lock, DB 조건과 동시성 test |
| [`policy-decision-client`](exercises/policy-decision-client/) | 외부 HTTP 오류, timeout, 제한된 retry와 Circuit Breaker |

### 선택 전문 프로젝트

- [`idempotent-operation-outbox`](exercises/idempotent-operation-outbox/)
- [`kafka-avro-contract`](exercises/kafka-avro-contract/)
- [`publication-service`](exercises/publication-service/)

실제 프로젝트에서 사용하지 않은 기술을 사후 필수 검증으로 만들지 않습니다.

## FAIL → Rewind

```text
Project PASS
→ exercise README와 test만 확인
→ Guide 없이 구현
→ FAIL이면 test와 상태를 먼저 조사
→ 관련 문서만 다시 읽기
→ 같은 실패를 검출하는 test를 남기고 재시도
```

## 저장소 구성

```text
.
├── README.md
├── docs/
│   ├── Stable Core 문서
│   └── JIT / Rewind 문서
└── exercises/
    ├── 필수 역량 검증 프로젝트
    ├── 전문 주제 프로젝트
    └── 통합 프로젝트 예제
```

## 완료 기준

- Java 진입 기준과 Spring Boot Stable Core를 충족합니다.
- 실제 Spring Boot 프로젝트 하나를 PASS합니다.
- 프로젝트에서 필요한 JIT 문서만 적용합니다.
- 필수 Competency Suite를 가이드 없이 통과합니다.
- 실패 뒤 DB 상태, 외부 효과와 resource가 어떻게 남는지 설명합니다.
- 실제 운영 host와 장기 장애를 검증하지 않았다면 미검사로 기록합니다.

## 범위 밖

Java 언어 전체, HTTP·SQL 일반 이론, 서비스 사이 Saga와 분산 합의, production infrastructure와 특정 산업 업무 규칙은 다른 가이드와 실제 프로젝트가 맡습니다.
