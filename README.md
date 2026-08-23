# 알고리즘 설계와 검증

이 브랜치는 특정 문제 유형의 풀이를 외우는 대신, 문제를 명확한 입력·출력 조건으로 바꾸고 적절한 자료구조와 알고리즘을 선택한 뒤 독립적인 기준 계산으로 결과를 검증하는 방법을 다룹니다.

```text
요구사항과 예외 조건을 정합니다.
→ 입력 크기에서 허용되는 시간·공간 비용을 계산합니다.
→ 필요한 상태와 자료구조를 선택합니다.
→ 정확성 근거를 적고 구현합니다.
→ 다른 계산 방법과 경계 입력으로 결과를 검증합니다.
```

문서는 특정 언어에 종속되지 않습니다. 필수 구현 프로젝트인 [`verified-algorithms`](exercises/verified-algorithms/)는 Python 3.12 이상을 사용합니다.

## 대상 독자와 선행 지식

다음 작업을 해 본 개발자를 대상으로 합니다.

- 한 언어로 함수, 조건문, 반복문과 기본 컬렉션을 사용합니다.
- 작은 프로그램을 실행하고 실패한 테스트를 읽습니다.
- 정수 범위와 입력 형식을 확인합니다.

Python 자체를 처음 배우는 과정은 [`python`](https://github.com/seungwoo7050/guides-archive/tree/python) 브랜치가 맡습니다. C++로 같은 내용을 구현하려면 `docs/90-implementation-profiles/cpp20.md`를 함께 사용합니다.

## 완료 후 갖춰야 할 능력

전체 과정을 마치면 다음 작업을 자료 없이 다시 수행할 수 있어야 합니다.

- 자연어 문제를 입력, 출력, 답 없음, 잘못된 입력과 동점 처리까지 포함한 조건으로 정리합니다.
- 최악·기대·상각 비용을 구분하고 복사, 재귀 호출 스택과 출력 크기까지 포함해 비용을 계산합니다.
- 반복 불변식, 귀납, 교환 논리, 절단 성질과 완화 근거로 구현의 정확성을 설명합니다.
- 배열, 해시, 스택, 큐, 덱, 힙, 트리와 서로소 집합을 필요한 연산과 비용에 따라 선택합니다.
- 완전탐색, 그리디와 동적 계획법을 적용할 수 있는 조건과 실패 반례를 구분합니다.
- BFS, Dijkstra, Bellman–Ford, Kruskal, 최대 유량과 KMP의 전제와 반환값을 설명하고 구현합니다.
- 작은 입력을 모두 계산하거나 다른 알고리즘을 사용해 독립적인 기준 결과를 만듭니다.
- 실패 입력을 줄여 최소 반례를 만들고 회귀 테스트로 남깁니다.

## 저장소 구성

```text
.
├── README.md
├── docs/
│   ├── 00-roadmap.md
│   ├── 01-foundations/
│   ├── 02-data-structures/
│   ├── 03-design-techniques/
│   ├── 04-graph-algorithms/
│   ├── 05-string-algorithms/
│   ├── 06-complexity/
│   ├── 80-extended-practice.md
│   └── 90-implementation-profiles/
└── exercises/
    └── verified-algorithms/
```

- `docs/`는 문제 분석, 정확성, 비용과 알고리즘 선택 기준을 설명합니다.
- `exercises/verified-algorithms/`는 서로 다른 알고리즘을 하나의 설치 가능한 패키지와 독립 검증으로 연결합니다.

## 정본 전체 과정

알고리즘 자체를 한 분야로 학습하려면 다음 순서를 사용합니다.

### 1. 문제 분석과 정확성

- [`문제 조건과 반례`](docs/01-foundations/01-problem-contracts-and-counterexamples.md)
- [`점근 분석`](docs/01-foundations/02-asymptotic-analysis.md)
- [`점화식과 분할 정복`](docs/01-foundations/03-recurrences-and-divide-and-conquer.md)
- [`정확성과 불변식`](docs/01-foundations/04-correctness-and-invariants.md)

### 2. 자료구조와 탐색

- [`선형 구조, 구간과 해시`](docs/02-data-structures/01-linear-structures-ranges-and-hashing.md)
- [`순서, 탐색, 힙과 우선순위`](docs/02-data-structures/02-order-search-heaps-and-priority.md)
- [`트리와 균형 탐색 트리`](docs/02-data-structures/03-trees-and-balanced-search-trees.md)
- [`서로소 집합과 상각 분석`](docs/02-data-structures/04-disjoint-sets-and-amortized-analysis.md)
- [`정렬, 안정성과 비교 하한`](docs/06-complexity/01-sorting-stability-and-lower-bounds.md)

### 3. 설계 기법

- [`완전탐색과 백트래킹`](docs/03-design-techniques/01-brute-force-and-backtracking.md)
- [`그리디 설계`](docs/03-design-techniques/02-greedy-methods.md)
- [`동적 계획법`](docs/03-design-techniques/03-dynamic-programming.md)

### 4. 그래프와 문자열

- [`그래프 순회와 위상 순서`](docs/04-graph-algorithms/01-traversal-and-topological-order.md)
- [`최소 스패닝 트리`](docs/04-graph-algorithms/02-minimum-spanning-trees.md)
- [`최단 경로`](docs/04-graph-algorithms/03-shortest-paths.md)
- [`네트워크 유량과 매칭`](docs/04-graph-algorithms/04-network-flow-and-matching.md)
- [`문자열 매칭과 전처리`](docs/05-string-algorithms/01-string-matching-and-preprocessing.md)

정확한 문서·구현 순서는 [`docs/00-roadmap.md`](docs/00-roadmap.md)를 따릅니다.

## 구현 프로젝트

필수 프로젝트는 [`verified-algorithms`](exercises/verified-algorithms/) 하나입니다.

이 프로젝트는 누적 합, lower bound, red-black tree 검증, 0/1 knapsack, 구간 선택, LCS, BFS, Dijkstra, Kruskal, Bellman–Ford, 최대 유량과 KMP를 제공합니다. 테스트는 후보 구현과 다른 계산 방법을 사용하며, 최적값뿐 아니라 선택한 간선과 유량 행렬처럼 결과를 설명하는 자료도 검사합니다.

```sh
cd exercises/verified-algorithms
python -m unittest discover -s tests -v
```

제공된 구현의 테스트가 통과하는 것만으로 완료하지 않습니다. 별도 복사본에서 구현을 보지 않고 공개 API와 테스트만 사용해 핵심 함수군을 다시 작성합니다.

## 다른 개발 트랙에서 사용하는 방법

이 절은 알고리즘 전체 과정을 줄여 이수하라는 뜻이 아닙니다. 실제 프로젝트에서 필요한 부분을 찾는 지도입니다.

### C/C++ 프로젝트

먼저 다음 문서를 사용합니다.

- 문제 조건과 반례
- 점근 분석
- 선형 구조, 해시, 탐색과 힙
- 정렬과 안정성

트리, 서로소 집합, 그래프와 동적 계획법은 현재 프로젝트가 해당 연산을 요구할 때 읽습니다.

### 웹 애플리케이션

다음 내용이면 대부분의 초기 프로젝트에 충분합니다.

- 입력 크기와 비용 계산
- 해시, 정렬, 탐색과 우선순위
- 페이지네이션, 구간 처리와 캐시 키에 필요한 기본 자료구조

그래프, 최대 유량과 고급 문자열 알고리즘은 실제 제품 기능이 요구할 때만 추가합니다.

### 게임 서버

다음 내용을 우선 사용합니다.

- 비용 계산과 실패 반례
- 큐, 덱, 힙과 해시
- 트리와 서로소 집합
- 경로 탐색, 매칭 또는 스케줄링이 필요한 경우 관련 그래프 절

실시간 tick이나 네트워크 전송 문제를 알고리즘 문제로만 환원하지 않습니다. 시간, 동시성, 상태 전송은 운영체제·네트워크·게임 서버 가이드에서 함께 검토합니다.

## 선택 심화

- [`복잡도 클래스와 환원`](docs/06-complexity/02-complexity-classes-and-reductions.md)
- [`확장 문제와 검증 설계`](docs/80-extended-practice.md)
- [`Python 구현 프로필`](docs/90-implementation-profiles/python.md)
- [`C++20 구현 프로필`](docs/90-implementation-profiles/cpp20.md)

선택 자료는 필수 구현이 끝난 뒤, 해당 문제를 실제로 다뤄야 할 때 사용합니다.

## 완료 기준

- 필수 문서의 알고리즘을 입력 조건과 비용에 따라 선택합니다.
- `verified-algorithms`의 전체 테스트를 통과합니다.
- 구현을 보지 않고 핵심 함수군을 다시 작성해 같은 검사를 통과합니다.
- 각 함수의 입력 조건, 정확성 근거, 시간·추가 공간과 독립 검증 방법을 설명합니다.
- 한 번 이상 실패 입력을 최소화해 회귀 테스트로 남깁니다.

## 범위 밖

이 브랜치만으로 모든 기업의 알고리즘 시험 유형이나 모든 제품의 성능 문제를 보장하지 않습니다. 특정 언어의 런타임 비용, 운영체제 스케줄링, 데이터베이스 실행 계획과 네트워크 지연은 해당 브랜치와 실제 프로젝트에서 별도로 확인합니다.
