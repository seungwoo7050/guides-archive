# 확장 문제와 검증 설계

이 문서는 필수 과정을 마친 뒤 범위를 넓히기 위한 선택 자료입니다. 문제 수를 늘리는 것이 목적이 아닙니다. 이미 익힌 알고리즘의 입력 조건이 달라졌을 때 상태, 정확성 근거, 기준 계산을 다시 설계하는 데 목적이 있습니다.

## 학습 목표

- 기존 알고리즘의 전조건이 바뀌었을 때 저장할 값과 정확성 근거를 다시 정합니다.
- 최적값뿐 아니라 실제 해, 존재 여부, 유일성, certificate를 검증합니다.
- 작은 입력의 전수 계산, 성질 기반 검사, 서로 다른 구현 중 적절한 방법을 고릅니다.
- overflow, timeout, 퇴화 입력처럼 반환값 밖의 실행 조건도 확인합니다.

## 선행지식

[`docs/00-roadmap.md`](00-roadmap.md)의 필수 과정을 완료하고, [`verified-algorithms`](../exercises/verified-algorithms/)의 구현을 보지 않고 다시 작성해 전체 테스트를 통과한 뒤 진행합니다.

## 문제 하나를 시작할 때 작성할 내용

```text
입력과 반환값: 답 없음, 잘못된 입력, 동점 처리까지 적습니다.
상태: 이후 결과를 결정하는 데 필요한 값을 적습니다.
정확성: 불변식, 교환 논리, 절단 성질, 귀납, 환원 중 필요한 근거를 적습니다.
비용: 입력 크기와 값의 표현 길이를 기준으로 시간·공간을 계산합니다.
기준 계산: 후보와 다른 방법으로 작은 입력의 정답을 구합니다.
실패 입력: 가정 하나를 깨는 최소 입력과 재현 명령을 남깁니다.
```

처음부터 효율적인 구현을 작성하지 않습니다. `n <= 8`처럼 가능한 답을 모두 검사할 수 있는 범위를 먼저 정하고, 기준 계산이 후보 구현과 parser·정렬 순서·핵심 helper를 공유하지 않게 합니다.

## 1. 구간, 순서와 탐색

### Sliding-window maximum

길이 `k`인 모든 창의 최댓값을 반환합니다. Monotonic deque에는 값이 아니라 index를 넣어야 창을 벗어난 원소를 판정할 수 있습니다.

확인할 내용:

- `k <= 0`, `k > n`, 빈 입력의 처리 방법
- deque의 index는 증가하고 해당 값은 감소한다는 불변식
- 같은 값이 반복될 때 오래된 index를 잘못 제거하는 결함
- 각 창을 직접 순회한 기준 결과

### 첫 비반복 원소의 위치

전체 빈도와 최초 위치를 따로 저장합니다. 전체 입력을 읽은 뒤 반환하는 함수인지, 현재까지 본 값만으로 streaming 결과를 내는 함수인지 먼저 정합니다.

기준 계산은 각 위치의 값을 전체 수열에서 다시 세는 단순한 방법을 사용합니다. Map에 마지막 위치를 저장해 최초 위치처럼 반환하는 결함을 검사합니다.

### 답에 대한 이분 탐색

작업을 `T`시간 안에 끝낼 수 있는지 판단하는 함수로 최소 시간을 찾습니다.

- 판정 함수가 어느 방향으로 단조인지 설명합니다.
- 답을 포함하는 상한을 모르면 overflow하지 않는 범위에서 두 배로 늘립니다.
- 작은 값부터 순서대로 검사한 결과를 기준으로 사용합니다.
- `middle`, 누적 생산량, 상한 계산의 overflow를 검사합니다.

### 3-way partition과 radix pass

중복이 많은 quicksort partition과 안정적인 radix pass를 비교합니다.

- Partition 뒤 `< pivot`, `== pivot`, `> pivot` 구간을 모두 확인합니다.
- Radix의 각 pass에서 같은 digit을 가진 record의 original id 순서가 유지되는지 확인합니다.
- 정렬 결과가 원본과 같은 multiset인지 검사합니다.

## 2. Tree와 시간에 따라 바뀌는 상태

### Rotation 검증기

BST subtree를 왼쪽 또는 오른쪽으로 rotation한 뒤 다음을 확인합니다.

1. inorder key 순서가 같습니다.
2. child와 parent link가 서로 일치합니다.
3. subtree 밖의 연결이 끊기지 않았습니다.
4. 저장한 height나 size가 독립적으로 다시 계산한 값과 같습니다.

작은 tree 모양을 생성해 가능한 모든 rotation 위치에 적용합니다.

### Order-statistics tree

각 subtree의 size를 저장해 `k`번째 원소와 rank를 구합니다.

- `k`를 0부터 셀지 1부터 셀지 정합니다.
- 삽입, 삭제, rotation 뒤 size를 갱신할 node를 정합니다.
- Inorder list의 index를 기준 결과로 사용합니다.
- 중복 key를 허용할지, count로 합칠지 정합니다.

### 삭제가 있는 연결성

기본 DSU는 이미 합친 component를 쉽게 나누지 못합니다. 모든 연산을 미리 알 수 있다면 시간을 거꾸로 읽어 삭제를 추가 연산으로 바꾸는 offline 방법을 검토합니다.

- 같은 간선이 여러 번 추가·삭제되는 경우를 정합니다.
- 각 시점의 작은 graph를 BFS로 다시 계산한 결과와 비교합니다.
- Rollback DSU를 사용하면 변경 stack과 snapshot 위치를 명확히 정합니다.

## 3. 그래프 확장

### 두 번째 spanning tree

MST와 다른 spanning tree 중 가장 작은 가중치를 구합니다.

- 같은 가중치의 서로 다른 MST가 있을 때 “두 번째”가 다른 edge set인지 더 큰 가중치인지 정합니다.
- 작은 graph에서 모든 `V-1`개 간선 조합을 검사합니다.
- 연결성과 cycle 여부를 확인한 뒤 가중치를 계산합니다.

### Bottleneck path

두 문제를 구분합니다.

- 경로에서 가장 큰 간선 가중치를 최소화합니다.
- 경로에서 가장 작은 간선 가중치를 최대화합니다.

일반 최단 경로처럼 가중치 합을 최소화하는 문제와 섞지 않습니다. 작은 simple path를 모두 열거해 기준 결과를 만듭니다. MST 경로 성질을 사용한다면 undirected graph 전조건을 적습니다.

### 정확히 `K`개 간선을 사용하는 최단 경로

상태를 `(사용한 간선 수, 정점)`으로 둡니다. 같은 정점이라도 사용한 간선 수가 다르면 이후 가능한 경로가 다릅니다.

- `dp[k][v]`가 정확히 `k`개인지 최대 `k`개인지 정합니다.
- 음수 간선을 허용해도 간선 수가 제한되어 상태 수는 유한합니다.
- 작은 graph에서 길이 `K`인 모든 walk를 열거합니다.

### 차분 제약과 arbitrage

부등식 `x_v <= x_u + w`를 간선 `u -> v`로 바꾸고 음수 cycle 여부로 해의 존재를 판정합니다. 환율 곱셈은 log를 사용해 합으로 바꿀 수 있습니다.

- 부동소수점 오차와 이익으로 인정할 임계값을 정합니다.
- 한 시작점에서 도달 가능한 cycle만 볼지 super source로 전체를 볼지 정합니다.
- 작은 cycle을 직접 열거한 결과와 비교합니다.

## 4. 문자열 확장

### 모든 겹치는 일치

첫 위치가 아니라 모든 일치 시작 위치를 반환합니다. KMP에서 한 번 일치한 뒤 상태를 0으로 만들면 겹치는 결과를 잃습니다.

- 빈 pattern의 결과를 `0..n` 전체 또는 오류 중 하나로 정합니다.
- 모든 시작 위치의 slice를 직접 비교합니다.
- `"aaaa"`에서 `"aa"`처럼 겹침이 많은 입력을 포함합니다.

### 최소 주기

Prefix function의 마지막 값으로 주기 후보를 계산하더라도 문자열 길이가 그 후보로 나누어지는지 확인해야 합니다.

- 반복 횟수 1도 주기로 허용할지 정합니다.
- 가능한 길이를 1부터 직접 검사한 결과와 비교합니다.
- 빈 문자열과 한 문자 입력을 따로 정합니다.

### Streaming KMP

본문이 여러 chunk로 들어와도 pattern 일치 상태를 유지합니다. Chunk를 나누는 위치가 결과를 바꾸면 안 됩니다.

- 같은 본문을 가능한 모든 두 chunk 분할로 전달합니다.
- 전체 본문을 한 번에 전달한 결과와 비교합니다.
- Byte stream과 Unicode text stream의 index 단위를 구분합니다.

## 5. Certificate, 환원과 flow 확장

### Certificate를 반환하는 알고리즘

값만 반환하던 함수가 실제 선택 집합이나 경로도 반환하도록 확장합니다. 검증기는 최적화 문제를 다시 풀지 않고 다음을 확인합니다.

- Certificate 크기가 입력 길이의 다항식입니다.
- 원본 입력의 제약을 만족합니다.
- 선언한 값과 certificate에서 계산한 값이 같습니다.
- 최적성은 작은 전수 계산이나 별도 bound로 확인합니다.

### Vertex splitting

정점 capacity가 있는 flow 문제에서 각 정점을 `v_in -> v_out`으로 나눕니다.

- 원본 간선 `u -> v`를 `u_out -> v_in`으로 바꿉니다.
- Source와 sink도 나눌지 정합니다.
- 무한 capacity 역할의 값은 가능한 총 flow보다 크고 자료형 범위를 넘지 않아야 합니다.
- 원본 경로와 변환한 network flow의 대응을 설명합니다.

### Lower-bound circulation

각 간선의 lower bound만큼 먼저 보낸 뒤 정점별 demand를 계산해 feasible circulation 문제로 바꿉니다.

- 입력에서 `0 <= lower <= upper`를 검사합니다.
- Demand 부호와 super source·sink 간선 방향을 작은 예제로 추적합니다.
- 반환 flow가 원래 lower·upper와 conservation을 만족하는지 다시 검사합니다.

### König 대응

Bipartite graph에서 maximum matching과 minimum vertex cover의 크기가 같다는 성질을 사용합니다.

- Matching 결과에서 alternating reachability를 계산합니다.
- 만든 cover가 모든 간선을 덮는지 검사합니다.
- 작은 graph의 모든 정점 부분집합을 열거해 최소 cover 크기와 비교합니다.

## 6. 문제 목록

아래 표는 구현 개수를 채우기 위한 목록이 아닙니다. 문제를 하나 고르면 고유 조건과 검증 결과를 모두 제출해야 합니다.

### 문제 조건과 선형 상태

| 문제 | 반드시 정할 조건 | 검증 결과 |
| --- | --- | --- |
| 목표 합의 첫 index 쌍 | 같은 원소 재사용 금지, 여러 답의 동점 처리 | `O(n²)` 기준 계산과 최초 index map 비교 |
| 서로 다른 값이 `K`개 이하인 최장 구간 | 빈 구간, `K=0`, 왼쪽 이동 뒤 빈도 제거 | 모든 구간 열거와 양끝 상태 추적 |
| 중복 없는 방문 기록 | 입력 순서 보존과 membership 분리 | set을 사용하지 않은 선형 기준 계산 |
| 단조 증가 구간의 끝 | strict와 non-strict 증가 구분 | 같은 값이 연속되는 최소 반례 |
| 괄호 오류 위치 | 잘못 닫힌 위치와 입력 종료 시 열린 괄호 구분 | stack 상태와 최초 오류 index |
| 다음 작업 완료 시각 | 같은 시각 작업의 결정적인 순서 | 작은 event simulation 기준 계산 |
| 가장 가까운 두 수 | 같은 값, 여러 최소 차이의 동점 처리 | 모든 쌍 열거와 정렬 scan 비교 |

### 분석, 상각과 정렬

| 문제 | 반드시 정할 조건 | 검증 결과 |
| --- | --- | --- |
| Inversion 개수 | 같은 값은 inversion이 아님 | 이중 반복문과 merge 기반 계산 비교 |
| 분할 정복 최대 부분 배열 | 빈 결과 허용 여부, 음수만 있는 입력 | 모든 구간 합 열거 |
| 빠른 모듈러 거듭제곱 | 음수 지수 거부, 곱셈 전 modulo | 지수 감소와 반복 기준 계산 |
| Fibonacci 호출 수 | 함수 호출 수와 산술 결과 비용 분리 | 호출 tree 점화식 전개 |
| Euclid 종료와 비용 | 나머지가 엄격히 감소 | 연속 Fibonacci 입력 추적 |
| 두 stack으로 만든 queue | 한 번의 이동과 연속 연산 비용 구분 | 각 원소의 이동 횟수 합계 |
| 두 배 확장 동적 배열 | `capacity`와 `size` 구분 | 실제 복사 횟수 합계 |
| Binary counter | 한 번의 최악 flip 수와 전체 flip 수 구분 | bit별 flip 횟수 표 |
| 축소 시 재할당 진동 | grow·shrink 임계값 사이의 여유 | 진동을 만드는 push·pop 입력 |
| 정렬 block 병합 | 원소가 참여하는 병합 단계 수 | binary counter와 potential 대응 |
| 거의 정렬된 입력의 insertion sort | inversion 수에 따른 비용 | shift 횟수와 inversion 수 비교 |
| 여러 key의 안정 정렬 | 낮은 우선순위 key부터 stable pass | original record id 순서 검사 |

### 균형 tree와 spanning 결과

| 문제 | 반드시 정할 조건 | 검증 결과 |
| --- | --- | --- |
| 삽입 가능한 red-black set | recolor와 rotation 뒤 모든 규칙 복원 | 각 삽입 prefix를 독립 validator로 검사 |
| 일반 BST의 최악 높이 | 삽입 순서와 높이 관계 | 정렬·역순·무작위 입력 비교 |
| key 구간 출력 | 결과 개수 `k`를 시간에 포함 | inorder filter 기준 계산과 `O(h+k)` 설명 |
| Red-black 삭제 | double-black 상태와 sentinel color | 삭제마다 전체 규칙 재검사 |
| Minimum·maximum spanning forest | 연결되지 않은 결과가 forest인지 확인 | component별 tree와 모든 조합 비교 |
| 이미 연결된 도로망 확장 | 기존 연결을 비용 0으로 반영 | 선행 `union` 또는 super-node 대응 |

### 경로, 문자열과 복잡도

| 문제 | 반드시 정할 조건 | 검증 결과 |
| --- | --- | --- |
| 음수 cycle 영향을 표시하는 거리 | cycle에서 도달 가능한 정점만 `-∞` | 추가 reachability 계산 |
| DAG 최단 경로 복원 | 음수 간선 허용, cycle 입력 거부 | topological order와 predecessor 추적 |
| Floyd–Warshall 경로 복원 | `next` 갱신과 도달 불가능 구분 | 복원 경로의 간선 합 재계산 |
| 검증을 포함한 Rabin–Karp | hash 일치 뒤 실제 문자 확인 | 작은 modulus 충돌 입력 |
| 문자열 회전 판정 | 길이가 같다는 전제와 빈 문자열 | 가능한 모든 rotation 직접 비교 |
| 모든 border 길이와 등장 횟수 | border chain과 prefix 빈도 누적 | 모든 prefix·suffix 직접 비교 |
| Vertex Cover verifier | 최적값을 다시 풀지 않고 cover만 검사 | 모든 간선 coverage와 certificate 크기 |
| 3-SAT에서 Clique로 환원 | clause마다 한 정점, 모순 literal 간선 제외 | assignment와 clique의 양방향 대응 |
| Independent Set과 Vertex Cover | 같은 graph에서 complement 관계 | 두 certificate 크기 합이 `|V|`인지 검사 |
| Subset Sum pseudo-polynomial DP | 숫자 값과 입력 bit 길이 구분 | `O(nT)`가 bit 길이 다항식이 아님을 설명 |
| Optimization과 decision oracle | threshold 질의 수와 실제 해 복원 | 이분 탐색과 self-reduction 호출 기록 |

### Flow 결과 복원

| 문제 | 반드시 정할 조건 | 검증 결과 |
| --- | --- | --- |
| 최대 유량과 최소 cut 복원 | residual graph에서 source가 도달 가능한 집합 | cut capacity와 flow 값 비교 |
| Maximum bipartite matching | 두 partition 검증과 unit capacity | 선택한 간선이 정점을 중복 사용하지 않음 |
| Minimum bipartite vertex cover | alternating path에서 cover 복원 | 모든 간선 coverage와 matching 크기 비교 |
| Maximum edge-disjoint path | 원본 간선 capacity가 1 | 복원한 경로끼리 간선을 공유하지 않음 |

## `verified-algorithms`와 연결하는 방법

새 문제를 기존 package의 공개 API에 억지로 추가하지 않습니다. 별도 임시 디렉터리에서 다음 자산만 재사용합니다.

- 입력 조건과 실패 결과를 적는 방식
- 고정 seed를 사용하는 방식
- 작은 전수 계산의 입력 상한
- 최적값과 certificate를 따로 검사하는 방식
- 실패 입력을 최소화해 회귀 테스트로 남기는 방식

기존 함수와 직접 연결되는 문제는 다음과 같습니다.

- 구간·탐색: `prefix_sums`, `lower_bound`
- Tree: `red_black_height`
- 최적화: `knapsack_01`, `select_intervals`, `lcs_length`
- 그래프·flow: `kruskal_mst`, `bellman_ford`, `max_flow`
- 문자열: `kmp_find`

## 완료 기준

- 서로 다른 영역에서 문제 세 개를 고릅니다.
- 각 문제에 입력·반환값, 상태, 정확성 근거, 시간·공간, 기준 계산을 작성합니다.
- 정상 입력, 경계 입력, 잘못된 입력, 의도적인 결함을 하나 이상 만듭니다.
- 전수 검사 범위나 random seed를 기록해 같은 실패를 다시 만들 수 있게 합니다.
- 후보 구현과 기준 계산이 parser, 핵심 helper, 상태 갱신을 공유하지 않는지 확인합니다.

## 실패 신호

- 문제 이름만 보고 기존 알고리즘을 그대로 적용하면서 바뀐 전조건을 적지 않습니다.
- 후보 구현의 출력을 그대로 저장해 기준 결과로 사용합니다.
- 전수 검사의 입력 상한이 없어 검증 코드 자체가 끝나지 않습니다.
- 최적값만 맞으면 잘못된 certificate, overflow, timeout도 성공으로 처리합니다.
- 여러 문제를 풀었지만 최소 반례와 실패 원인을 남기지 않습니다.

## 권장 진행 순서

1. 효율적인 풀이를 보기 전에 작은 기준 계산의 입력 상한을 정합니다.
2. 입력, 반환값, 답 없음, 잘못된 입력, 동점 처리를 적습니다.
3. 의도적인 결함 구현을 하나 만들고 기준 계산이 거부하는 최소 입력을 찾습니다.
4. 후보 구현을 작성해 작은 입력 공간이나 고정 seed 표본과 비교합니다.
5. 입력 크기를 키워 정한 시간 안에 종료하는지 확인합니다.
6. 코드를 닫고 정확성 근거와 비용을 다시 설명합니다.
