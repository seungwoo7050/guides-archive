# 컴퓨터 구조 가이드

이 브랜치는 값의 비트 표현부터 명령 실행, 메모리 접근, 비순차 실행과 멀티코어 일관성까지 연결합니다. 특정 CPU 제품의 기능을 외우는 대신, 프로그램에 보이는 동작과 프로세서 내부 모델, 성능 비용과 실제 관찰 결과를 구분하는 것을 목표로 합니다.

## 대상 독자와 선행 지식

- 한 언어로 정수, 배열, 함수와 반복문을 사용합니다.
- 명령행에서 프로그램을 빌드하고 실행합니다.
- 고정된 입력으로 테스트를 실행하고 실패 결과를 읽습니다.

C 관찰 예제를 이해하려면 C의 기본 문법이 필요합니다. Python 실습은 표준 라이브러리만 사용합니다.

## 완료 후 갖춰야 할 능력

- 고정 폭 정수와 IEEE 754 값의 비트 표현을 설명합니다.
- ISA가 정하는 동작과 프로세서 내부 구현을 구분합니다.
- 명령 수, CPI와 클록 주기로 실행 시간을 설명합니다.
- 데이터 경로와 파이프라인의 전달, 정지와 잘못 가져온 명령 제거를 추적합니다.
- 캐시와 TLB가 저장하는 값과 실패 조건을 구분합니다.
- 비순차 실행에서 실행 완료와 프로그램 순서 반영을 구분합니다.
- 여러 코어가 같은 캐시 라인을 사용할 때 MESI 상태와 거짓 공유를 설명합니다.
- 상태 모델과 실제 CPU 측정이 각각 보장하는 범위를 구분합니다.

## 저장소 구성

```text
.
├── README.md
├── docs/
├── examples/
└── exercises/
    └── processor-model/
```

- `docs/`는 개념, 계산과 상태 변화를 설명합니다.
- `examples/`는 컴파일러와 실행 환경에서 나타나는 성능 차이를 관찰합니다.
- `processor-model`은 핵심 내용을 결정적인 Python 상태 모델로 검증합니다.

## 정본 전체 과정

### 1. 표현, ISA와 성능식

- [`데이터 표현과 산술`](docs/01-representation-and-isa/01-data-representation-and-arithmetic.md)
- [`ISA, 어셈블리와 프로그램 실행`](docs/01-representation-and-isa/02-isa-assembly-and-program-execution.md)
- [`성능, CPI와 Amdahl 법칙`](docs/01-representation-and-isa/03-performance-cpi-and-amdahl.md)

### 2. 순차 실행

- [`데이터 경로와 제어`](docs/02-in-order-execution/04-datapath-and-control.md)
- [`파이프라인 위험 요소와 분기`](docs/02-in-order-execution/05-pipeline-hazards-and-branching.md)

### 3. 메모리 계층

- [`캐시, 지역성과 AMAT`](docs/03-memory-hierarchy/06-cache-locality-and-amat.md)
- [`주소 변환과 TLB`](docs/03-memory-hierarchy/07-address-translation-and-tlb.md)

### 4. 현대 CPU와 멀티코어

- [`슈퍼스칼라, 비순차 실행과 추측`](docs/04-parallel-execution/08-superscalar-out-of-order-and-speculation.md)
- [`멀티코어 일관성과 거짓 공유`](docs/04-parallel-execution/10-multicore-coherence-and-false-sharing.md)

[`SIMD, 벡터화와 데이터 배치`](docs/04-parallel-execution/09-simd-vectorization-and-data-layout.md)는 선택 문서입니다.

## 필수 실습 프로젝트

[`processor-model`](exercises/processor-model/)은 다음 상태를 하나의 프로젝트에서 연결합니다.

```text
고정 폭 비트 표현
→ Tiny-RISC 실행
→ 성능식
→ 제어 신호
→ 5단계 파이프라인
→ 캐시
→ 주소 변환과 TLB
→ 분기 예측기와 재정렬 버퍼
→ MESI 일관성
```

```sh
cd exercises/processor-model
make check
make demo
```

각 모듈을 무조건 처음부터 다시 작성할 필요는 없습니다. 소스와 검사를 읽고 입력을 바꾸어 실행한 뒤, 상태가 바뀌는 이유와 잘못된 상태가 거부되는 이유를 설명해야 합니다.

## 관찰 예제

| 예제 | 확인하는 내용 |
|---|---|
| [`branch-benchmark`](examples/branch-benchmark/) | 입력 패턴과 분기 명령의 관계 |
| [`layout-benchmark`](examples/layout-benchmark/) | 순회 순서와 공간 지역성 |
| [`false-sharing`](examples/false-sharing/) | 서로 다른 값이 같은 캐시 라인에 있을 때의 경합 |
| [`vectorization-report`](examples/vectorization-report/) | 컴파일러 벡터화 보고서와 결과 검증 |

실행 시간만으로 결론을 내리지 않습니다. 컴파일러가 만든 코드, 검사 합계, 입력 크기와 반복 측정 결과를 함께 봅니다.

## 다른 개발 트랙에서 사용하는 방법

### C/C++ 시스템 개발

다음을 우선 사용합니다.

- 데이터 표현과 산술
- ISA와 프로그램 실행
- 성능식
- 캐시와 지역성
- 주소 변환과 TLB
- 멀티코어 일관성과 거짓 공유

파이프라인과 비순차 실행의 상세 모델은 성능 원인을 더 깊게 조사할 때 확장합니다.

### 웹 개발

일반 웹 프로젝트의 선행 과정은 아닙니다. 다음 문제가 실제로 나타났을 때 필요한 절만 사용합니다.

- 정수 범위와 부동소수점 오류
- 데이터 배치와 캐시 영향
- 멀티스레드 런타임의 거짓 공유
- 성능 측정 결과를 CPU·I/O·대기 시간으로 구분하는 작업

### 게임 서버

다음을 권장합니다.

- 성능식과 측정
- 캐시와 데이터 배치
- 멀티코어 일관성과 거짓 공유
- 필요하면 비순차 실행과 SIMD

서버 tick 지연을 CPU 구조만으로 설명하지 않습니다. lock 대기, 네트워크, 메모리 할당과 저장소 I/O를 함께 측정합니다.

## 권장 진행 방식

문서를 전부 읽은 뒤 실습을 한꺼번에 실행하지 않습니다. 개념을 읽은 직후 `processor-model`의 해당 명령과 관찰 예제를 확인합니다. 세부 순서는 [`docs/00-roadmap.md`](docs/00-roadmap.md)를 따릅니다.

## 완료 기준

- `processor-model`의 전체 검사가 통과합니다.
- 주어진 명령과 추적 입력의 주요 상태 변화를 설명합니다.
- cache miss, TLB miss, page fault와 coherence invalidation을 구분합니다.
- 실행 완료와 프로그램 순서 반영을 같은 개념으로 설명하지 않습니다.
- 모델이 생략한 조건과 실제 CPU 측정의 변동 요인을 명시합니다.

## 범위 밖

프로세서 RTL 설계, 특정 제조사의 비공개 내부 상태, GPU 설계, 운영체제의 전체 메모리 관리자와 언어별 lock-free 알고리즘 증명은 포함하지 않습니다.
