# C++20 구현 프로필

## 목적

이 문서는 C++ 문법 과정이 아닙니다. 알고리즘 문서의 입력 조건과 상태를 C++20으로 옮길 때 자주 발생하는 정수 범위, iterator 수명, comparator, 복사 비용, 재귀 깊이를 정리합니다.

`verified-algorithms`의 공식 구현과 테스트는 Python 3.12용입니다. C++20으로 같은 알고리즘을 작성할 때는 별도 test harness를 만들어 같은 조건을 검증해야 합니다.

## 빌드 기준

먼저 경고를 모두 확인합니다.

```sh
c++ -std=c++20 \
  -Wall -Wextra -Wpedantic -Wconversion \
  -g main.cpp -o program
```

성능 측정 전에 AddressSanitizer와 UndefinedBehaviorSanitizer를 실행합니다.

```sh
c++ -std=c++20 \
  -Wall -Wextra -Wpedantic -Wconversion \
  -fsanitize=address,undefined \
  -fno-omit-frame-pointer -g \
  main.cpp -o program
```

## 자료구조 대응

| 알고리즘 개념 | C++20 도구 | 확인할 점 |
| --- | --- | --- |
| 동적 배열 | `std::vector` | 재할당 뒤 iterator, pointer, reference가 무효화될 수 있습니다. |
| queue·deque | `std::queue`, `std::deque` | container adapter가 제공하는 연산만 사용합니다. |
| min-heap | `std::priority_queue`와 comparator | 기본 `priority_queue`는 max-heap입니다. |
| ordered set·map | `std::set`, `std::map` | 일반적인 연산은 `O(log n)`입니다. |
| hash set·map | `std::unordered_set`, `std::unordered_map` | 기대 비용, `reserve`, key hash를 확인합니다. |
| 이분 탐색 | `std::lower_bound` | 반열린 iterator 구간을 사용합니다. |
| 도달 불가능 거리 | `std::optional<long long>` | 큰 sentinel의 덧셈 overflow를 피할 수 있습니다. |

## 정수 범위

대입 대상이 `long long`이어도 피연산자가 `int`라면 곱셈이 먼저 `int`에서 수행될 수 있습니다.

```cpp
long long product = 1LL * left * right;
```

입력 상한으로 다음 값을 계산한 뒤 자료형을 고릅니다.

- 합의 최댓값과 최솟값
- 거리의 최댓값
- 경우의 수
- 가중치 × 간선 수
- 이분 탐색 상한

Signed integer overflow는 정의되지 않은 동작입니다. wraparound를 기대하지 않습니다.

## index와 크기

`container.size()`는 unsigned 계열을 반환합니다. `-1` sentinel과 섞으면 비교 결과가 의도와 달라질 수 있습니다.

위치가 없음을 표현할 때는 다음 중 하나를 선택합니다.

- `std::optional<std::size_t>`
- `container.size()`를 명시적인 반환값으로 사용
- signed index와 `-1`을 사용하되 변환 위치를 제한

중간 index는 overflow를 피하도록 계산합니다.

```cpp
const auto middle = low + (high - low) / 2;
```

## iterator와 reference 수명

`std::vector`가 재할당되면 기존 원소를 가리키는 iterator, pointer, reference가 무효화될 수 있습니다.

다음 코드는 위험할 수 있습니다.

```cpp
auto& current = values.front();
values.push_back(next);  // 재할당되면 current가 무효화될 수 있습니다.
```

삽입 전에 `reserve`할 수 있는지, index로 다시 접근할 수 있는지, 다른 container가 필요한지 확인합니다.

Local object의 주소나 reference를 함수 밖으로 반환하지 않습니다.

## comparator

정렬과 ordered container의 comparator는 strict weak ordering을 만족해야 합니다.

```cpp
return std::tie(a.primary, a.secondary)
     < std::tie(b.primary, b.secondary);
```

다음을 피합니다.

- `<=`를 comparator로 사용합니다.
- 비교 중 바뀌는 외부 상태를 참조합니다.
- 두 값의 차이를 반환해 정수 overflow를 일으킵니다.
- floating-point `NaN`을 일반 값처럼 순서화합니다.

동점 처리 방식이 반환 결과의 일부라면 comparator에 두 번째 key를 명시합니다.

## `std::priority_queue`

기본은 큰 값이 먼저 나오는 max-heap입니다. Min-heap은 다음처럼 만들 수 있습니다.

```cpp
using Item = std::pair<long long, int>;
std::priority_queue<
    Item,
    std::vector<Item>,
    std::greater<Item>
> queue;
```

Dijkstra에서는 같은 정점의 오래된 거리 항목이 남을 수 있습니다. 꺼낸 거리와 현재 distance가 다르면 확장하지 않습니다.

## 재귀와 stack

그래프 DFS나 편향 tree는 깊이가 `O(n)`이 될 수 있습니다. C++은 tail-call optimization을 보장하지 않습니다.

입력 상한이 크면 명시적인 `std::vector` 또는 `std::stack`을 사용합니다. Postorder라면 node와 처리 단계를 함께 저장합니다.

## 복사와 이동

- 큰 container를 읽기만 할 때는 `const&`로 받습니다.
- 함수가 값을 소유해야 한다면 value로 받은 뒤 move하는 방식을 검토합니다.
- 단순한 구간 관찰에는 iterator pair나 `std::span`을 사용할 수 있습니다.
- 반복문 안에서 container를 값으로 반환하거나 복사하지 않습니다.

Copy elision이 일어날 수 있어도 알고리즘 분석에서 의도하지 않은 `O(n)` 복사를 무시하지 않습니다.

## 그래프 간선과 수명

Single-pass input을 여러 번 사용해야 한다면 `std::vector<Edge>`에 저장합니다. Iterator가 가리키는 원본 container가 함수 실행 동안 살아 있는지도 확인합니다.

인접 list를 만들 때 정점 수로 먼저 크기를 정하고 모든 source·target index를 검사합니다.

```cpp
std::vector<std::vector<Edge>> graph(vertex_count);
```

## 결정적인 결과

`std::unordered_*`의 iteration 순서를 반환 순서로 사용하지 않습니다.

- 결과 순서가 필요하면 정렬합니다.
- 같은 priority에는 두 번째 key를 둡니다.
- MST처럼 여러 정답이 가능한 경우 최적값과 certificate 조건을 따로 검사합니다.

## 입출력과 핵심 함수 분리

```cpp
Result solve(const Input& input);
```

Parsing과 출력은 `main`에 두고 알고리즘은 명확한 값과 반환형을 가진 함수로 분리합니다. 그래야 작은 기준 계산과 같은 입력으로 비교하기 쉽습니다.

## Python 기준과 비교하는 방법

C++ 구현은 Python package의 공식 PASS와 같은 결과로 자동 인정되지 않습니다. 같은 조건을 검증하려면 다음 중 하나를 사용합니다.

- C++ 안에 작은 exhaustive oracle을 별도로 작성합니다.
- 고정된 text 또는 JSON 형식으로 같은 입력을 Python과 C++에 전달합니다.
- 각 구현의 출력을 비교하고 실패 입력을 고정합니다.

Adapter가 parser나 정렬 helper를 두 구현에 공유하면 독립성이 낮아질 수 있습니다.

## 확인표

- 정수 합과 곱이 자료형 범위 안에 있습니까?
- unsigned 크기와 음수 sentinel을 섞지 않았습니까?
- `vector` 재할당 뒤 무효화된 reference를 사용하지 않습니까?
- comparator가 strict weak ordering을 만족합니까?
- 재귀 깊이가 입력 상한을 감당합니까?
- 큰 container가 의도치 않게 복사되지 않습니까?
- hash container의 순서를 결과 순서로 사용하지 않습니까?
- sanitizer 검사를 통과했습니까?
