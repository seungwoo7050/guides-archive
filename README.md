# 데이터베이스 시스템

이 브랜치는 관계형 데이터베이스의 논리적 의미, 저장 방식, 동시성, 복구, 실행 계획과 안전한 변경을 연결합니다. SQL 문법만 익히는 입문 과정도 아니고, 모든 개발자에게 저장 엔진 구현을 선행 조건으로 요구하는 과정도 아닙니다.

학습 목적에 따라 다음 두 경로를 제공합니다.

```text
애플리케이션 데이터 경로
    정확한 SQL·제약·트랜잭션·인덱스·마이그레이션

DBMS 내부구조 경로
    page·index·buffer pool·MVCC/WAL·질의 실행
```

두 경로를 모두 마치면 애플리케이션의 질의와 DBMS 내부 동작을 하나의 요청에서 연결해 설명할 수 있습니다.

## 대상 독자와 선행 지식

- 간단한 table을 만들고 `SELECT`, `INSERT`, `UPDATE`, `DELETE`를 작성합니다.
- Python 프로젝트와 테스트를 실행합니다.
- Docker Engine과 Docker Compose를 사용할 수 있으면 PostgreSQL 실습을 수행할 수 있습니다.

SQL 자체가 처음이라면 먼저 작은 애플리케이션 프로젝트에서 기본 CRUD를 사용한 뒤 돌아오는 편이 낫습니다.

## 공통 완료 능력

- relation, tuple, key와 SQL의 bag 의미를 구분합니다.
- `NULL`, 외부 조인, 집계와 정렬에서 생기는 오류를 찾습니다.
- 업무 규칙을 key, foreign key, `UNIQUE`, `CHECK`, `NOT NULL`로 표현합니다.
- lost update, write skew, deadlock과 재시도 조건을 확인합니다.
- 논리 질의와 물리 실행 계획을 구분합니다.
- schema와 index를 기존 데이터와 실행 중 요청을 고려해 변경합니다.

내부구조 경로를 추가로 마치면 다음도 수행합니다.

- tuple이 record와 page에 저장되는 과정을 추적합니다.
- B+ tree의 탐색, 분할과 범위 조회를 설명합니다.
- buffer pool의 pin, dirty, 교체와 flush 순서를 추적합니다.
- MVCC, WAL, LSN, REDO와 UNDO를 장애 시점별로 설명합니다.
- join 알고리즘과 실행 비용을 비교합니다.

## 저장소 구성

```text
.
├── README.md
├── docs/
└── exercises/
    ├── sql-semantics-views/
    ├── ticketing-database/
    ├── slotted-page/
    ├── bplus-tree/
    ├── clock-buffer-pool/
    ├── postgres-concurrency-guards/
    ├── wal-recovery-simulator/
    ├── join-algorithms/
    ├── postgres-workload-indexes/
    └── mini-storage-engine/
```

## 경로 A — 애플리케이션 데이터

웹, 백엔드와 게임 서비스에서 관계형 데이터베이스를 안전하게 사용하려면 이 경로를 먼저 선택합니다.

```text
관계 모델과 SQL 의미
→ schema와 제약
→ transaction과 동시 실행
→ index와 실행 계획
→ 안전한 migration과 backfill
```

### 필수 실습

- [`sql-semantics-views`](exercises/sql-semantics-views/)
- [`ticketing-database`](exercises/ticketing-database/)
- [`postgres-concurrency-guards`](exercises/postgres-concurrency-guards/)
- [`postgres-workload-indexes`](exercises/postgres-workload-indexes/)

### 완료 후 할 수 있어야 하는 일

- 업무 규칙을 schema 제약과 transaction으로 표현합니다.
- 동시 요청에서 잃어버린 갱신과 write skew를 재현합니다.
- 실제 실행 계획과 측정 결과를 보고 index를 선택합니다.
- 필드 추가, 기존 데이터 채우기, 검증과 이전 형식 제거 순서를 설계합니다.

## 경로 B — DBMS 내부구조

저장 엔진, 데이터베이스 성능, 복구와 내부 구현을 학습하려면 이 경로를 선택합니다.

```text
page와 record
→ B+ tree
→ buffer pool
→ MVCC와 WAL 복구
→ join 실행
```

### 필수 실습

- [`slotted-page`](exercises/slotted-page/)
- [`bplus-tree`](exercises/bplus-tree/)
- [`clock-buffer-pool`](exercises/clock-buffer-pool/)
- [`wal-recovery-simulator`](exercises/wal-recovery-simulator/)
- [`join-algorithms`](exercises/join-algorithms/)

애플리케이션 개발자가 이 경로 전체를 프로젝트 진입 전에 수행할 필요는 없습니다. page, WAL 또는 join 비용을 실제로 조사해야 할 때 해당 실습부터 시작할 수 있습니다.

## 전체 통합 경로

두 경로를 모두 마치면 다음 순서로 종합 검토합니다.

```text
하나의 ticket 생성 요청
→ schema와 transaction
→ record와 page
→ index와 buffer pool
→ WAL과 장애 복구
→ 조회 plan과 결과 검증
```

[`mini-storage-engine`](exercises/mini-storage-engine/)은 page, buffer pool, WAL과 index를 한 프로그램으로 연결하는 선택 통합 프로젝트입니다. 전용 실습을 대체하지 않습니다.

## 문서 지도

정확한 문서 순서는 [`docs/00-roadmap.md`](docs/00-roadmap.md)에 있습니다.

- 관계 의미와 설계: `docs/01-*`
- 저장과 index: `docs/02-*`
- transaction과 복구: `docs/03-*`
- 질의 실행과 최적화: `docs/04-*`
- 통합 검토: `docs/05-capstones/`

## 다른 개발 트랙에서 사용하는 방법

### 웹·백엔드

경로 A를 사용합니다. 다음 문제가 나타나면 경로 B의 일부를 JIT로 읽습니다.

- page와 row 크기 때문에 I/O가 증가함
- index 구조와 범위 조회 비용을 더 깊게 설명해야 함
- WAL, checkpoint와 장애 복구를 조사해야 함
- join 전략과 메모리 사용을 분석해야 함

### 게임 서버

계정, 경제, inventory, matchmaking metadata와 replay metadata에는 경로 A가 우선입니다. 실시간 match state를 관계형 DB에 매 tick 저장하지 않습니다. snapshot, event, cache와 장기 보존의 역할을 먼저 나누고 필요한 transaction과 index만 사용합니다.

### 데이터베이스 엔지니어링

두 경로 전체와 `mini-storage-engine`을 권장합니다.

## 실행과 검증

각 프로젝트는 자신의 디렉터리에서 실행합니다.

```sh
cd exercises/<project>
make test
```

PostgreSQL 프로젝트에는 Docker Engine과 Docker Compose v2가 필요합니다. 자동 검사가 통과하더라도 실제 운영 데이터 크기, backup 자동화, replication과 장애 조치를 검증한 것은 아닙니다.

## 완료 기준

### 애플리케이션 경로

- 경로 A의 필수 프로젝트를 통과합니다.
- schema, transaction, index와 migration 선택을 근거로 설명합니다.
- 느린 조회, deadlock과 backfill에서 먼저 확인할 자료를 정합니다.

### 내부구조 경로

- 경로 B의 필수 프로젝트를 통과합니다.
- page, index, buffer pool, WAL과 join의 상태 변화를 설명합니다.
- 잘못된 구현이 어떤 검사에서 거부되는지 설명합니다.

### 전체 과정

두 경로의 기준을 모두 만족하고 하나의 요청을 논리 의미에서 저장·복구·조회 계획까지 추적합니다.

## 범위 밖

특정 ORM 사용법, 운영 backup 자동화, replication, sharding, 분산 transaction과 특정 DBMS 전체 소스 분석은 포함하지 않습니다. 이러한 주제는 실제 서비스나 전문 과정에서 이어서 학습합니다.
