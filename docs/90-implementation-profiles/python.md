# Python 구현 프로필

## 목적

이 문서는 알고리즘 개념을 다시 설명하지 않습니다. 핵심 문서의 입력 조건과 의사코드를 Python으로 옮길 때 자주 놓치는 자료형, 실행 비용, 재귀, mutable state, 테스트 방식을 정리합니다.

## 기준 환경

- Python 3.12 이상
- 표준 library만으로 runtime 실행
- package build에 `setuptools>=68` 사용
- type hint는 함수가 기대하는 값을 설명하지만 runtime validation을 대신하지 않습니다.

## 자료구조 대응

| 알고리즘 개념 | Python 도구 | 확인할 점 |
| --- | --- | --- |
| 동적 배열 | `list` | 앞쪽 `pop(0)`은 `O(n)`입니다. |
| queue·deque | `collections.deque` | 양끝 삽입·삭제를 `O(1)`에 처리합니다. |
| min-heap | `heapq` | decrease-key 대신 새 항목을 넣고 오래된 항목을 버리는 방식을 자주 사용합니다. |
| set·map | `set`, `dict` | 기대 비용과 key의 불변성을 확인합니다. |
| 이분 탐색 | `bisect` | 반환값이 첫 삽입 위치인지 확인합니다. |
| 도달 불가능 거리 | `None`, `math.inf` | 덧셈과 비교 전에 별도 처리합니다. |

## 정수 연산

Python 정수는 고정 폭 overflow가 발생하지 않지만 값이 커질수록 연산 비용도 증가합니다. 큰 정수의 덧셈과 곱셈을 무조건 `O(1)`이라고 가정하지 않습니다.

Python에서 동작하는 코드가 C나 C++에서도 같은 범위를 안전하게 처리한다고 일반화하지 않습니다. 다른 언어로 옮길 때는 입력 상한으로 합과 곱의 최댓값을 계산합니다.

## index와 slice

- `sequence[a:b]`는 반열린 구간을 사용합니다.
- `list`와 문자열 slice는 새 객체를 만들며 길이에 비례한 시간이 듭니다.
- 존재하지 않는 위치를 `-1`로 표현할 때 실제 Python 음수 index와 혼동하지 않습니다.
- `range(start, stop)`도 `stop`을 포함하지 않습니다.

반복문 안에서 slice를 계속 만들면 의도하지 않은 `O(n²)` 복사가 생길 수 있습니다.

## 재귀와 명시적인 stack

Python의 기본 recursion limit은 깊은 DFS나 편향 tree를 처리하기에 충분하지 않을 수 있습니다. 단순히 limit을 크게 올리기 전에 명시적인 stack을 검토합니다.

Postorder를 반복으로 구현한다면 node만 저장하지 말고 다음에 방문할 child 위치나 처리 단계를 함께 저장합니다.

```python
stack = [(root, False)]
```

`False`는 처음 들어온 상태, `True`는 자식을 처리하고 돌아온 상태처럼 사용할 수 있습니다.

## heap의 동점과 stale entry

`heapq`는 tuple을 앞에서부터 비교합니다. Priority가 같을 때 뒤의 object끼리 비교할 수 없다면 `TypeError`가 발생합니다.

```python
heapq.heappush(heap, (priority, sequence, item))
```

증가하는 `sequence`를 두 번째 값으로 사용하면 동점 순서를 결정적으로 만들 수 있습니다.

Dijkstra처럼 같은 정점의 여러 거리 후보를 넣는 경우에는 `pop`한 거리와 현재 distance 배열을 비교해 오래된 항목을 버립니다.

## mutable state와 복사

- 2차원 배열은 `[[0] * width for _ in range(height)]`로 만듭니다.
- `[[0] * width] * height`는 같은 row 객체를 여러 번 참조합니다.
- default mutable argument를 사용하지 않습니다.
- 백트래킹에서 `append`했다면 해당 branch가 끝난 뒤 `pop`합니다.
- 후보 구현과 기준 계산에 같은 mutable 입력 객체를 공유하지 않습니다.

```python
def collect(values: list[int] | None = None) -> list[int]:
    if values is None:
        values = []
    return values
```

## 문자열

- 반복문 안에서 문자열을 계속 `+=`하면 중간 문자열이 반복해서 만들어질 수 있습니다.
- 여러 조각은 `list`에 모아 `"".join(parts)`로 합칩니다.
- Python 문자열 index는 Unicode code point에 가깝지만 사용자가 보는 grapheme cluster와 항상 같지는 않습니다.
- byte 위치가 필요한 protocol parser에서는 `bytes`를 사용합니다.

## 함수와 입출력을 분리합니다

기업형 알고리즘 문제에서는 parsing과 핵심 알고리즘을 분리하는 편이 테스트하기 쉽습니다.

```python
def solve(data: str) -> str:
    ...

if __name__ == "__main__":
    import sys

    sys.stdout.write(solve(sys.stdin.read()))
```

가능하면 내부 계산은 문자열 입출력보다 명확한 매개변수와 반환값을 가진 함수로 작성합니다.

## 결정적인 결과

`dict`가 insertion order를 보존하더라도 결과 순서가 함수 조건이라면 그 사실을 우연한 구현 세부사항에 맡기지 않습니다.

- 반환 순서가 필요하면 명시적으로 정렬합니다.
- heap의 동점 key를 정합니다.
- set iteration 순서를 출력 순서로 사용하지 않습니다.
- 무작위 테스트는 고정 seed를 사용합니다.

## 검증

고정된 random generator를 사용합니다.

```python
source = random.Random(20260201)
```

실패하면 seed만 남기지 말고 실제 입력을 출력해 회귀 테스트에 추가합니다.

작은 입력에서는 다음 방법을 사용할 수 있습니다.

- `itertools.combinations`로 부분집합을 열거합니다.
- `itertools.product`로 작은 값 조합을 열거합니다.
- `bisect_left`, `str.find` 같은 표준 함수와 비교합니다.
- 그래프의 모든 간선 조합이나 cut을 입력 크기를 제한해 검사합니다.

## `verified-algorithms` 실행

프로젝트 디렉터리에서 테스트합니다.

```sh
cd exercises/verified-algorithms
python -m unittest discover -s tests -v
```

설치된 package로 확인하려면 다음 명령을 사용합니다.

```sh
python -m pip install --no-build-isolation .
python -c "import verified_algorithms"
```

Package source는 `src/verified_algorithms/`에 있습니다. `tests/test_algorithms.py`는 별도 설치 없이 `src/`를 import path에 추가해 실행할 수 있습니다.

## 성능 확인표

- queue에 `list.pop(0)`을 사용하지 않았습니까?
- 반복문 안에서 큰 slice나 정렬을 만들지 않았습니까?
- membership에 `list` 선형 탐색을 의도적으로 사용했습니까?
- 같은 정점의 오래된 heap 항목을 버립니까?
- 깊은 재귀가 입력 상한을 넘지 않습니까?
- 큰 상태 공간에서 tuple과 object 생성량이 과도하지 않습니까?
- 결과 순서가 hash container의 iteration 순서에 의존하지 않습니까?
