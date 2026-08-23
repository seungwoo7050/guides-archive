# 분산 서비스의 실패와 복구

이 브랜치는 서비스를 여러 개로 나누는 방법보다, 서비스가 나뉜 뒤 생기는 실패를 어떻게 처리할지 다룹니다.

네트워크 호출은 응답이 없더라도 상대 서비스가 이미 상태를 바꿨을 수 있습니다. 같은 요청과 이벤트가 다시 도착할 수 있고, 전달 순서가 바뀔 수 있으며, 정본 상태와 조회용 복제본은 한동안 다를 수 있습니다. 이 과정에서는 이를 예외적인 사고가 아니라 정상적으로 들어올 수 있는 조건으로 취급합니다.

## 시작 시점과 선행 지식

이 브랜치는 단일 프로세스나 단일 서비스 프로젝트의 공통 선행 과정이 아닙니다. 다음 조건이 생긴 뒤 시작하는 편이 적절합니다.

- 두 개 이상의 서비스가 네트워크로 상태 변경을 요청합니다.
- 메시지 전달, 재시도나 비동기 처리가 필요합니다.
- 한 요청의 결과를 즉시 확정할 수 없는 경우가 있습니다.
- 정본 상태와 조회 모델 또는 캐시가 서로 다른 시점을 봅니다.

다음 지식이 필요합니다.

- Java의 클래스, 컬렉션, 예외와 기본 테스트
- HTTP 요청·응답과 데이터베이스 transaction의 기본 개념
- 메시지 브로커가 메시지를 보관하고 구독자에게 전달한다는 수준의 이해

Spring Boot와 Kafka 운영 경험은 필수 조건이 아닙니다.

## 완료 후 갖춰야 할 능력

- 데이터마다 정본과 유일한 변경 주체를 정합니다.
- timeout과 업무 실패를 구분하고 `PENDING`, `UNKNOWN`, `ACCEPTED`, `REJECTED`를 사용합니다.
- 같은 요청이나 이벤트가 다시 들어와도 업무 효과를 한 번만 적용합니다.
- 상태 변경과 Outbox를 함께 저장하고 중단 뒤 남은 작업을 다시 처리합니다.
- event ID, schema version과 aggregate sequence를 검증합니다.
- 조회 모델 적용 뒤 checkpoint를 전진시키고 전체 기록으로 다시 구축합니다.
- 전체 deadline 안에서 재시도를 제한하고 과부하에서 대기열을 무한히 늘리지 않습니다.
- request, operation, event, trace, correlation과 causation ID를 구분합니다.
- 정본과 파생 상태가 같은 최종 결과에 도달했는지 검증합니다.

## 저장소 구성

```text
.
├── README.md
├── docs/
└── exercises/
```

각 `exercises/<project>/`는 다른 디렉터리의 빌드 설정에 의존하지 않는 독립 프로젝트입니다.

## 정본 전체 과정

### 1. 상태 소유자와 확정할 수 없는 결과

문서:

- [`부분 실패와 확정할 수 없는 결과`](docs/01-boundaries-and-failure/01-partial-failure-and-uncertain-outcomes.md)
- [`서비스 경계와 데이터 소유권`](docs/01-boundaries-and-failure/02-service-boundaries-and-data-ownership.md)
- [`동기·비동기 결정`](docs/01-boundaries-and-failure/03-synchronous-and-asynchronous-decisions.md)

프로젝트:

- [`service-boundary`](exercises/service-boundary/)
- [`request-decision`](exercises/request-decision/)

### 2. 중복 전달과 상태 수렴

문서:

- [`멱등 처리와 단일 업무 효과`](docs/02-delivery-and-consistency/01-idempotency-and-single-effects.md)
- [`Outbox, Saga와 재조정`](docs/02-delivery-and-consistency/02-outbox-saga-and-reconciliation.md)
- [`계약, 버전과 순서`](docs/02-delivery-and-consistency/03-contracts-versioning-and-order.md)
- [`조회 모델과 늦은 이벤트`](docs/02-delivery-and-consistency/04-read-models-and-late-events.md)

프로젝트:

- [`outbox-reconciliation`](exercises/outbox-reconciliation/)
- [`contracts-and-order`](exercises/contracts-and-order/)
- [`read-model-rebuild`](exercises/read-model-rebuild/)

### 3. 재시도와 과부하 제한

문서:

- [`timeout, retry, Circuit Breaker와 DLQ`](docs/03-resilience-and-load/01-timeouts-retries-circuit-breakers-and-dlq.md)
- [`backpressure, bulkhead와 load shedding`](docs/03-resilience-and-load/02-backpressure-bulkheads-and-load-shedding.md)

프로젝트:

- [`retry-budget`](exercises/retry-budget/)
- [`backpressure`](exercises/backpressure/)

### 4. 식별자와 최종 검증

문서:

- [`분산 관측성`](docs/04-release-and-evidence/02-distributed-observability.md)

프로젝트:

- [`observability-correlation`](exercises/observability-correlation/)
- [`reservation-flow`](exercises/reservation-flow/)

`reservation-flow`는 정본 상태, Outbox, 중복 전달, 순서가 바뀐 조회 모델, 재조정과 제한된 dispatcher를 하나의 예약 처리 과정에 연결합니다.

## 다른 개발 트랙에서 사용하는 방법

### 웹·백엔드

단일 서비스로 기능을 완성할 수 있는 단계에서는 이 브랜치를 먼저 수행하지 않습니다. 다음 문제가 실제로 생기면 관련 절부터 시작합니다.

| 문제 | 먼저 볼 내용 |
|---|---|
| timeout 뒤 성공 여부를 모름 | 확정할 수 없는 결과, operation ID |
| 같은 요청이 다시 들어옴 | 멱등 처리와 단일 효과 |
| DB 변경과 이벤트 발행을 함께 처리해야 함 | Outbox와 재조정 |
| 조회 모델이 늦거나 순서가 바뀜 | 계약·순서와 read model rebuild |
| 재시도로 장애가 커짐 | retry budget과 backpressure |

### 게임 서버

다음 영역에서 사용합니다.

- 계정, inventory, 경제와 matchmaking 상태의 유일한 변경 주체
- match 생성 요청과 서버 배치 결과를 즉시 확정할 수 없는 경우
- 경기 결과, 보상과 통계 이벤트의 중복 전달
- lobby·match·결제 서비스 사이의 Outbox와 재조정
- 접속 폭주와 match 생성 요청의 backpressure

실시간 방 안의 tick, 명령 순서와 snapshot은 game-server 브랜치가 맡습니다.

### 플랫폼·클라우드

비동기 provisioning, 반복 reconcile과 작업 상태를 다룰 때 operation ID, 멱등 처리, 제한된 재시도와 관측 식별자를 적용합니다. Kubernetes나 cloud control plane 자체는 별도 과정에서 다룹니다.

## 선택 자료

### 개념을 좁게 다시 확인하는 프로젝트

- [`uncertain-outcome`](exercises/uncertain-outcome/)
- [`duplicate-delivery`](exercises/duplicate-delivery/)

### 심화 검증

- [`종단 간 장애 근거`](docs/04-release-and-evidence/03-end-to-end-chaos-and-failure-evidence.md)
- [`chaos-evidence`](exercises/chaos-evidence/)
- [`통합 과제`](docs/05-capstone.md)

### 릴리스·성능·Kafka

- [`다중 저장소 릴리스 manifest`](docs/04-release-and-evidence/01-multi-repository-builds-and-release-manifests.md)
- [`release-manifest`](exercises/release-manifest/)
- [`성능 기준과 주장`](docs/04-release-and-evidence/04-performance-gates-and-claims.md)
- [`performance-gate`](exercises/performance-gate/)
- [`단일 broker KRaft`](docs/90-optional-labs/01-single-broker-kraft.md)
- [`single-broker-kraft`](exercises/single-broker-kraft/)

## 실행 방법

Java 프로젝트는 각 디렉터리에서 실행합니다.

```sh
make build
make test
make clean
```

Kafka 통합 검사는 Docker Engine과 Docker Compose v2가 필요합니다. 실행하지 못한 통합 검사는 통과로 기록하지 않습니다.

## 완료 기준

- 필수 프로젝트의 테스트를 통과합니다.
- 각 상태를 어느 서비스가 바꾸는지 설명합니다.
- operation ID와 event ID를 어디까지 유지하는지 설명합니다.
- Outbox 전송 중 중단됐을 때 남는 상태를 추적합니다.
- 중복 이벤트가 업무 상태를 두 번 바꾸지 않는 이유를 테스트로 보입니다.
- `UNKNOWN`을 실패나 성공으로 임의 해석하지 않습니다.
- 정본과 조회 모델의 수렴 조건을 명시합니다.

## 범위 밖

분산 합의, 복제 로그, sharding, 브로커 운영과 특정 프레임워크 사용법은 직접 다루지 않습니다. 이 브랜치는 서비스 사이의 실패, 전달과 상태 수렴에 집중합니다.
