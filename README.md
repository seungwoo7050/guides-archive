# 사이버보안 분석·검증·대응

이 브랜치는 보안을 도구 이름이나 공격 기법 목록으로 배우지 않습니다. 시스템이 지켜야 할 상태를 정하고, 그 상태가 깨질 수 있는 조건을 찾은 뒤, 허가된 합성 환경에서 필요한 만큼만 확인합니다. 확인한 문제는 요구사항, 수정, 회귀 검사, 탐지와 복구까지 연결합니다.

```text
보호할 상태와 근거를 정합니다.
→ 자산, 행위자와 신뢰 지점을 기준으로 위협을 작성합니다.
→ 허가된 범위에서 최소한만 검증합니다.
→ 원인을 수정하고 정상·경계·실패 사례를 다시 검사합니다.
→ 거절 이벤트와 경보로 같은 시도를 관찰합니다.
→ 사고 뒤 신뢰할 수 있는 상태를 다시 만듭니다.
```

## 대상 독자와 선행 지식

이 과정은 프로그래밍, 운영체제와 네트워크 입문을 대신하지 않습니다. 다음 작업을 수행할 수 있어야 합니다.

- 기존 애플리케이션과 서비스 코드를 읽습니다.
- JSON과 Markdown을 수정합니다.
- Python 테스트를 실행하고 실패 결과를 읽습니다.
- 허가된 대상과 허용한 행동을 문서로 고정합니다.

## 완료 후 갖춰야 할 능력

- 보안 목표를 주체, 자원, 행동과 허용 상태가 드러나는 문장으로 작성합니다.
- 사실, 가설과 결론을 구분하고 각 근거가 보장하는 범위를 설명합니다.
- 자산, 행위자의 능력, 신뢰 지점과 상태 변화를 연결해 위협을 작성합니다.
- 대상, identity, 허용 행동, 요청량과 중단 조건을 고정한 뒤 합성 데이터로 검증합니다.
- 인증, 객체 권한, service identity와 credential 수명을 구분합니다.
- 위협을 검증 가능한 요구사항과 정상·경계·실패 사례로 바꿉니다.
- 증상만 막는 수정과 공통 원인을 제거하는 수정을 구분합니다.
- 조사 가능한 보안 이벤트와 중복·지연·누락에 견디는 탐지 결과를 설계합니다.
- 사고 중 사실, 결정과 조치를 분리하고 제한, 원인 제거와 복구를 구분합니다.

## 저장소 구성

```text
.
├── README.md
├── docs/
└── exercises/
    └── ledgerlab-policy/
```

## 정본 전체 과정

### 1. 보안 판단과 안전한 검증

- [`보안 상태와 근거`](docs/01-security-state-and-evidence.md)
- [`자산, 신뢰 지점과 위협 모델`](docs/02-assets-trust-boundaries-and-threat-models.md)
- [`범위, 허가와 검증 규칙`](docs/03-scope-authorization-and-rules-of-engagement.md)

### 2. 실제 실패 형태

- [`위험, 취약점과 우선순위`](docs/04-risk-vulnerability-and-prioritization.md)
- [`애플리케이션 입력·권한 실패`](docs/06-application-boundary-failures.md)
- [`시스템 identity와 비밀값`](docs/07-system-identity-and-secret-boundaries.md)

### 3. 요구사항, 검사와 수정

- [`보안 요구사항과 지켜야 할 상태`](docs/10-security-requirements-and-design-invariants.md)
- [`보안 테스트와 판정 근거`](docs/11-security-testing-and-assurance.md)
- [`수정, 강화와 회귀 검사`](docs/12-remediation-hardening-and-regression.md)

### 4. 탐지와 복구

- [`telemetry, 탐지와 조사`](docs/13-telemetry-detection-and-investigation.md)
- [`사고 대응과 복구`](docs/14-incident-response-and-recovery.md)

## 필수 실습

[`ledgerlab-policy`](exercises/ledgerlab-policy/README.md)는 합성 보고서와 작업자 객체에 대한 접근 가능 여부를 판정합니다.

- 소유자, tenant와 완료 상태를 함께 확인하는 접근 판정
- service identity, job, 만료 시각과 폐기 여부를 확인하는 credential 판정
- 문자열 일부가 아니라 path segment를 비교하는 객체 범위 검사
- 확인할 수 없는 상태의 기본 거절
- 입력 상태를 바꾸지 않는 판정 함수
- 안정된 `reason_code`와 조사 가능한 authorization event
- 중복과 입력 순서에 영향을 받지 않는 correlation 단위 경보
- 정상 기능과 알려진 오답을 함께 구분하는 테스트

## 다른 개발 트랙에서 사용하는 방법

### 웹·백엔드

다음을 프로젝트와 함께 사용합니다.

- 애플리케이션 입력과 객체 권한
- 사용자 identity와 service identity
- 비밀값 수명
- 보안 요구사항과 회귀 검사
- 거절 이벤트, 조사와 복구

보안 가이드를 모두 끝낸 뒤 웹 프로젝트를 시작하지 않습니다. 인증, 권한, 외부 입력 또는 비밀값이 실제 구현에 나타나는 시점에 관련 절을 적용합니다.

### C/C++ 시스템 프로그램

이 브랜치는 메모리 안전 취약점 전체를 가르치지 않습니다. 다음 내용에 집중합니다.

- 보호할 상태와 신뢰 지점
- 파일, 프로세스와 service identity
- 허가된 검증 범위
- 실패 뒤 안전한 상태와 회귀 검사

언어 수준 메모리·객체 수명은 `c`와 `cpp` 브랜치가 맡습니다.

### 게임 서버

다음을 우선 사용합니다.

- 클라이언트를 신뢰하지 않는 상태 변경 규칙
- 사용자·서버·운영 도구 identity 분리
- 객체 권한과 credential 수명
- abuse 사건을 조사할 수 있는 이벤트
- 사고 중 제한, 원인 제거와 안전한 복구

게임 규칙 검증과 anti-cheat의 세부 탐지 기법은 game-server 프로젝트 요구에 맞춰 별도로 설계합니다.

## 선택 문서

- [`공격 표면과 경로`](docs/05-attack-surface-and-paths.md)
- [`공급망과 빌드 신뢰`](docs/08-supply-chain-and-build-trust.md)
- [`취약점 검증과 보고`](docs/09-vulnerability-validation-and-reporting.md)
- [`릴리스 전 보안 검토`](docs/15-security-review-and-release-decision.md)
- [`표준 지도`](docs/90-standards-map.md)

## 완료 기준

- 보안 목표와 위협을 구체적인 상태와 행동으로 작성합니다.
- 허가된 범위와 중단 조건을 먼저 고정합니다.
- `ledgerlab-policy`의 전체 테스트를 통과합니다.
- 잘못된 허용, 만료 경계, 누락된 identity와 중복 이벤트를 재현합니다.
- 수정 뒤 같은 실패를 검출하는 회귀 테스트를 남깁니다.
- 실제로 확인하지 않은 플랫폼과 공격 경로를 통과한 것으로 표현하지 않습니다.

## 범위 밖

프로그래밍 입문, 운영체제·네트워크 전체, 조직 규제 인증, 무허가 대상 검증과 특정 공격 도구 숙련은 포함하지 않습니다. 실제 대상의 검증은 명시적인 권한과 안전 규칙 아래에서만 수행합니다.
