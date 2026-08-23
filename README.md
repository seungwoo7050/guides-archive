# 클라우드 컴퓨팅 기초

이 브랜치는 특정 공급자의 제품명이나 콘솔 사용법을 외우지 않고, 클라우드 자원의 상태, 변경 권한, 장애 범위, 비용, 데이터 수명과 삭제 결과를 근거로 서비스를 판단하는 방법을 다룹니다.

문서와 [`local-cloud-model`](exercises/local-cloud-model/README.md)을 함께 완료하면 외부 유료 계정 없이도 이 학습 범위의 핵심 개념을 검증할 수 있습니다. 실제 공급자별 제한, 대규모 서비스 운영과 플랫폼 엔지니어링은 필요한 업무가 생겼을 때 이어서 학습합니다.

## 대상 독자와 선행 지식

다음 내용을 설명하거나 사용할 수 있어야 합니다.

- Linux에서 프로세스가 실행되고 포트를 여는 과정
- DNS, TLS, 애플리케이션, 데이터베이스, 로그와 백업의 역할
- Git, Markdown, JSON과 Python 표준 라이브러리
- 장애가 발생했을 때 마지막 성공 단계와 첫 실패 단계를 나누는 방법

클라우드 계정, 신용카드, Kubernetes 경험은 필요하지 않습니다. 필수 실습은 외부 네트워크와 유료 자원을 사용하지 않습니다.

## 완료 후 갖춰야 할 능력

- IaaS, PaaS, SaaS와 VM, 컨테이너, FaaS를 서로 다른 분류 기준으로 설명합니다.
- 원하는 상태, 공급자가 관리하는 상태, 실행 중 상태, 업무 데이터와 점검 근거를 구분합니다.
- control plane 권한과 data plane 권한을 따로 검토합니다.
- compute, network, storage와 identity의 수명과 의존 관계를 자원 목록으로 정리합니다.
- 복제본 수만 세지 않고 같은 원인으로 함께 실패하는 자원을 찾습니다.
- availability와 durability, RTO와 RPO, 복제와 백업을 구분합니다.
- 관리형 서비스가 대신하는 작업과 사용자가 계속 확인해야 하는 작업을 구분합니다.
- FaaS의 timeout, 동시 실행, 재전달과 중복 효과를 처리합니다.
- tenant ID가 데이터, 캐시, 작업, 내보내기와 삭제 과정에서 빠지지 않는지 확인합니다.
- 비용 유형, quota와 정리되지 않은 자원을 구분합니다.
- workload의 상태, 장애, 비용과 운영 능력을 기준으로 실행 방식을 비교합니다.

## 저장소 구성

```text
.
├── README.md
├── docs/
└── exercises/
    └── local-cloud-model/
```

- `docs/`는 클라우드 서비스의 상태, 권한, 장애와 비용을 판단하는 기준을 제공합니다.
- `exercises/local-cloud-model/`은 tenant, 자원, 이벤트와 삭제 상태를 결정적으로 검증합니다.

## 정본 전체 과정

처음에는 [`docs/00-roadmap.md`](docs/00-roadmap.md)를 읽습니다.

### 1. 판단 기준

1. [`클라우드 상태, 담당자와 점검 근거`](docs/01-cloud-state-responsibility-and-evidence.md)
2. [`클라우드 특성, 서비스 모델과 배포 모델`](docs/02-cloud-characteristics-service-and-deployment-models.md)

### 2. 권한과 자원 수명

3. [`control plane, data plane과 identity`](docs/03-control-plane-data-plane-and-identity.md)
4. [`IaaS compute, network와 storage`](docs/04-iaas-compute-network-and-storage.md)
5. [`SaaS tenancy와 격리`](docs/09-saas-tenancy-and-isolation.md)

### 3. 장애와 관리형 실행

6. [`장애 범위, 탄력성과 복구`](docs/05-failure-domains-elasticity-and-recovery.md)
7. [`PaaS와 관리형 서비스`](docs/06-paas-and-managed-service-contracts.md)
8. [`serverless와 FaaS runtime`](docs/07-serverless-and-faas-runtime.md)
9. [`이벤트 전달, 동시 실행과 멱등 처리`](docs/08-event-delivery-concurrency-and-idempotency.md)

### 4. 운영 판단

10. [`클라우드 보안, 관측과 사고`](docs/11-cloud-security-observability-and-incidents.md)
11. [`비용, 용량, quota와 FinOps`](docs/12-cost-capacity-quotas-and-finops.md)
12. [`서비스 선택과 설계 검토`](docs/14-service-selection-and-architecture-review.md)

문서를 모두 읽은 뒤 실습을 시작하지 않습니다. 자원과 tenant 상태를 읽은 뒤 모델의 해당 부분을 확인하고, 이벤트 전달 문서를 읽은 뒤 처리 부분을 이어서 검증합니다.

## 필수 실습

[`local-cloud-model`](exercises/local-cloud-model/README.md)은 다음 동작을 코드와 테스트로 확인합니다.

- tenant별 문서와 자원 상태 분리
- active document 수를 기준으로 한 quota 검사
- 다른 tenant의 문서 읽기와 덮어쓰기 거부
- `(tenant_id, event_id)` 단위 이벤트 식별
- 중복 이벤트의 단일 결과와 단일 사용량 반영
- 제한된 재시도와 dead letter 이동
- tenant 삭제 뒤 문서, 결과, queue와 자원 정리
- 문서 본문을 노출하지 않는 결정적 점검 결과

```sh
cd exercises/local-cloud-model
python3 -m unittest discover -s tests -v
python3 -m compileall -q local_cloud_model tests
```

## 다른 개발 트랙에서 사용하는 방법

### 웹·백엔드 개발

서비스를 로컬에서 구현한 뒤 실제 클라우드 실행 방식을 선택해야 할 때 사용합니다.

- 서비스 모델과 공유 책임
- control/data plane과 identity
- 장애 범위와 복구
- 관리형 서비스의 보장 범위
- 비용, quota와 삭제 결과

모든 FaaS·SaaS 문서를 프로젝트 전에 읽지 않습니다. 실제 실행 방식이 정해진 뒤 필요한 절만 확인합니다.

### 게임 서버

다음 문제가 생겼을 때 사용합니다.

- match server와 상태 저장소가 같은 원인으로 함께 실패하는지 검토
- 자동 확장과 실제 남은 처리 용량 구분
- 관리형 데이터 서비스의 책임 범위 확인
- 서버와 운영 도구의 workload identity 분리
- 고정 비용과 사용량 비용 비교

실시간 tick, 상태 복제와 재접속 자체는 game-server와 computer-networks에서 다룹니다.

### 플랫폼 엔지니어링

클라우드 자원의 공통 제공 경로를 설계한다면 전체 과정을 권장합니다. 다만 Kubernetes, IaC module, GitOps와 조직용 self-service platform은 별도 전문 과정이 필요합니다.

## 선택 자료

- [`SaaS entitlement, metering와 billing`](docs/10-saas-entitlements-metering-and-billing.md)
- [`이식성, lock-in과 exit`](docs/13-portability-lock-in-and-exit.md)
- [`표준 지도`](docs/90-standards-map.md)

## 검증 한계

`local-cloud-model`은 상태와 실패 조건을 결정적으로 확인합니다. 실제 공급자의 IAM, 가용 영역, 네트워크, 과금, 제한량과 장애 조치는 검증하지 않습니다. 확인하지 않은 공급자 동작을 통과한 것으로 기록하지 않습니다.

## 완료 기준

- 필수 문서의 검토 질문에 구체적인 자원과 실패 결과로 답합니다.
- `local-cloud-model`의 각 상태가 필요한 이유를 설명합니다.
- 다른 tenant 접근, quota 초과, 중복 이벤트, 재시도 한도와 tenant 삭제를 재현합니다.
- 서비스 선택 검토를 수행하고 로컬 모델이 확인하지 못하는 항목을 구분합니다.

## 범위 밖

특정 공급자의 전문가 과정, Kubernetes 운영, 대규모 SaaS 운영, 실제 비용 최적화와 조직 단위 보안 감사를 포함하지 않습니다. 이러한 내용은 실제 업무와 전문 브랜치에서 이어서 학습합니다.
