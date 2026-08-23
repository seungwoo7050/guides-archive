# 운영체제 원리 가이드

운영체제는 CPU, 메모리, 저장장치와 장치를 여러 실행 주체가 함께 사용하도록 관리합니다. 이 브랜치는 특정 커널의 명령이나 내부 자료구조를 외우는 대신, 운영체제가 유지하는 상태, 후보를 고르는 기준, 자원 수명과 장애 중에도 지켜야 할 조건을 학습합니다.

## 대상 독자와 선행 지식

- 한 언어로 상태를 표현하고 단위 테스트를 실행합니다.
- 프로세스, 파일과 메모리라는 용어를 사용해 본 경험이 있습니다.
- Python 3.10 이상, POSIX `sh`와 `make`를 사용할 수 있습니다.

C 관찰 예제에는 C11 compiler, POSIX thread와 Unix 계열 실행 환경이 필요합니다.

## 완료 후 갖춰야 할 능력

- system call, exception, fault와 interrupt를 발생 원인과 재개 위치로 구분합니다.
- process와 thread의 `READY`, `RUNNING`, `BLOCKED`, `TERMINATED` 전이를 추적합니다.
- FCFS, SJF, priority, round-robin과 MLFQ를 response time, waiting time, throughput과 공정성으로 비교합니다.
- race condition, data race, atomicity, visibility와 ordering을 구분합니다.
- lost wakeup, cancellation, deadlock, starvation, livelock과 priority inversion을 분석합니다.
- address space, mapping, PTE와 physical frame을 구분하고 page fault 결과를 설명합니다.
- page cache에 보이는 값과 장애 뒤 남는 값을 구분합니다.
- 장치 요청, DMA, interrupt, cancellation과 결과 회수 사이의 자원 수명을 추적합니다.
- 모순된 snapshot을 거부하고 위반한 조건을 설명합니다.

## 저장소 구성

```text
.
├── README.md
├── docs/
├── examples/
└── exercises/
    └── kernel-model/
```

## 정본 전체 과정

운영체제 자체를 학습하려면 다음 11개 문서를 모두 사용합니다.

### 1. 커널 진입과 실행 상태

- [커널 경계와 사건](docs/01-boundary-and-execution/01-kernel-boundary-and-events.md)
- [프로세스, 스레드와 문맥 전환](docs/01-boundary-and-execution/02-processes-threads-and-context-switches.md)
- [블록, 깨우기와 IPC](docs/01-boundary-and-execution/04-blocking-wakeup-and-ipc.md)
- [CPU 스케줄링](docs/01-boundary-and-execution/03-cpu-scheduling.md)

### 2. 동시성과 진행 보장

- [경쟁, 원자성과 순서](docs/02-concurrency/01-races-atomicity-and-ordering.md)
- [동기화 도구와 조건 대기](docs/02-concurrency/02-synchronization-primitives.md)
- [데드락과 진행 보장](docs/02-concurrency/03-deadlock-and-progress.md)

### 3. 가상 메모리

- [주소 공간과 page fault](docs/03-virtual-memory/01-address-spaces-and-faults.md)
- [요구 페이징, COW와 page replacement](docs/03-virtual-memory/02-demand-paging-cow-and-replacement.md)

### 4. 저장장치와 장치 I/O

- [파일시스템, page cache와 장애 일관성](docs/04-storage-and-io/01-filesystems-page-cache-and-crash-consistency.md)
- [장치 I/O, interrupt와 DMA](docs/04-storage-and-io/02-device-io-interrupts-and-dma.md)

## 필수 실습

[`kernel-model`](exercises/kernel-model/README.md)은 다음 상태를 결정적으로 실행하는 Python 시뮬레이터입니다.

- 실행 주체의 상태와 queue 위치
- condition generation과 semaphore handoff
- CPU scheduling과 metric
- deadlock 탐지와 safe sequence
- demand paging, COW와 page replacement
- filesystem durability와 journal recovery
- 장치 요청, DMA pin, cancellation과 completion
- JSON CLI와 잘못된 snapshot 거부

```sh
make -C exercises/kernel-model check
```

실제 커널과 hardware timing을 재현하지 않습니다. 같은 입력에서 같은 상태 전이를 만들기 때문에 원리와 잘못된 상태를 검증하는 데 사용합니다.

## 관찰 예제

```sh
make -C examples check
make -C examples verify
make -C examples sanitizer-check
```

예제는 system call 반환값, lost update, condition wait, lock order, `fork` 뒤 값 분리와 minor fault 변화를 관찰합니다. 특정 커널 내부 구현을 관찰 결과만으로 단정하지 않습니다.

## 다른 개발 트랙에서 사용하는 방법

### C/C++ 시스템 개발

다음을 우선 사용합니다.

- 커널 진입과 process/thread
- blocking, wakeup과 IPC
- race, synchronization과 deadlock
- address space와 page fault
- 파일시스템 수명과 장애 뒤 상태

장치 I/O와 DMA는 실제 시스템 프로그래밍 문제가 생겼을 때 확장합니다.

### 웹·백엔드

전체 과정을 선행할 필요는 없습니다. 다음 내용부터 사용합니다.

- 프로세스와 thread
- blocking과 wakeup
- race, cancellation과 자원 제한
- page cache와 파일 durability가 필요한 경우 해당 절

웹 요청, 데이터베이스 transaction과 네트워크 timeout은 해당 전문 브랜치와 함께 봅니다.

### 게임 서버

다음을 권장합니다.

- process/thread와 문맥 전환
- scheduling과 시간 지연
- synchronization, lost wakeup과 deadlock
- cancellation과 종료
- address space와 page fault
- 파일 durability와 장치 I/O는 snapshot·replay 저장 문제가 생겼을 때 사용

실시간 deadline을 일반 CPU scheduling 지식만으로 보장할 수 있다고 표현하지 않습니다.

## 선택 확장

[`확장 상태·binary image 실습`](docs/80-extended-labs.md)은 page-table 계산, MLFQ trace, 학습용 filesystem image와 descriptor ring을 다룹니다.

## 완료 기준

- 필수 문서 11개의 핵심 질문에 답합니다.
- `kernel-model`의 전체 검사를 통과합니다.
- 정상 scenario의 결과와 invalid snapshot이 거부되는 이유를 설명합니다.
- scheduling, COW, crash recovery와 cancellation 중 하나를 처음부터 끝까지 추적합니다.
- 고정된 모델 결과와 실행 환경에 따라 달라지는 관찰값을 구분합니다.

## 범위 밖

실제 kernel module·device driver, 특정 운영체제의 전체 소스, real-time scheduling, NUMA load balancing, 실제 filesystem format, production kernel debugging과 lock-free memory reclamation은 포함하지 않습니다.
