# 모바일 애플리케이션 개발

이 브랜치는 웹 애플리케이션을 만들어 본 개발자가 Android와 iOS에서 동작하는 모바일 앱을 설계하고 검증하는 데 필요한 기반을 다룹니다. 기준 구현은 TypeScript, React Native와 Expo를 사용하지만 특정 프레임워크 API를 외우는 것이 목적은 아닙니다.

앱 프로세스가 종료되거나 네트워크가 끊기고 권한이 철회되는 상황에서도 사용자가 저장한 내용을 보존하고, 설치된 네이티브 바이너리와 JavaScript 코드가 서로 호환되는지 판단할 수 있는 수준을 목표로 합니다.

## 대상 독자와 선행 지식

다음 경험을 전제로 합니다.

- TypeScript와 React로 작은 웹 애플리케이션을 구현합니다.
- HTTP 요청, 인증 상태와 외부 입력 검증을 이해합니다.
- 패키지 설치, 타입 검사와 테스트를 실행합니다.

웹 기초가 부족하면 `web-application`을 먼저 사용합니다. 모바일 앱의 서버 API, 인증과 데이터 저장소 운영은 별도 백엔드 프로젝트가 맡습니다.

## 완료 후 갖춰야 할 능력

- JavaScript 프로세스, 설치된 네이티브 바이너리와 운영체제가 소유하는 상태를 구분합니다.
- 화면 상태와 프로세스 종료 뒤 남아야 하는 상태를 나눕니다.
- 딥 링크, 알림과 복원된 경로를 검증한 뒤 현재 저장 상태에 맞는 화면을 엽니다.
- record 변경과 outbox 명령 생성을 하나의 SQLite transaction으로 처리합니다.
- 응답 유실, 중복 전송, 순서 역전, 인증 만료와 버전 충돌 뒤에도 사용자 변경을 보존합니다.
- 카메라, 사진 선택기와 위치 기능의 가용 여부와 권한 상태를 따로 처리합니다.
- 백그라운드 작업을 보장된 일정이 아니라 제한된 실행 기회로 다룹니다.
- Android와 iOS의 설정, 빌드 결과, 앱 식별 정보, runtimeVersion, 서명과 배포 근거를 구분합니다.
- 모델·어댑터·통합 테스트와 실제 기기 검사가 확인하는 범위를 구분합니다.

## 저장소 구성

```text
.
├── README.md
├── docs/
│   ├── 00-roadmap.md
│   ├── 01-mobile-runtime-and-project-boundaries.md
│   ├── 02-layout-input-and-accessibility.md
│   ├── 03-navigation-links-and-state-restoration.md
│   ├── 04-networking-session-and-error-contracts.md
│   ├── 05-local-data-offline-and-sync.md
│   ├── 06-permissions-device-capabilities-and-privacy.md
│   ├── 07-background-work-notifications-and-lifecycle.md
│   ├── 08-native-boundary-kotlin-swift-and-builds.md
│   ├── 09-testing-performance-and-observability.md
│   └── 10-release-signing-updates-and-store-delivery.md
└── exercises/
    └── field-notes/
```

## 정본 전체 과정

다음 문서는 최소 완료 경로에 포함합니다.

1. [`학습 로드맵`](docs/00-roadmap.md)
2. [`모바일 runtime과 프로젝트 구분`](docs/01-mobile-runtime-and-project-boundaries.md)
3. [`배치, 입력과 접근성`](docs/02-layout-input-and-accessibility.md)
4. [`화면 이동, 링크와 상태 복원`](docs/03-navigation-links-and-state-restoration.md)
5. [`로컬 데이터, 오프라인과 동기화`](docs/05-local-data-offline-and-sync.md)
6. [`권한, 기기 기능과 개인정보`](docs/06-permissions-device-capabilities-and-privacy.md)
7. [`백그라운드 작업, 알림과 수명`](docs/07-background-work-notifications-and-lifecycle.md)
8. [`네이티브 경계, Kotlin·Swift와 빌드`](docs/08-native-boundary-kotlin-swift-and-builds.md)
9. [`테스트, 성능과 관측`](docs/09-testing-performance-and-observability.md)
10. [`릴리스, 서명, 업데이트와 스토어 전달`](docs/10-release-signing-updates-and-store-delivery.md)

[`네트워크, 세션과 오류`](docs/04-networking-session-and-error-contracts.md)는 HTTP 응답 분류, 인증 정보 수명, 401 처리와 오래된 응답이 익숙하지 않을 때 보강합니다.

## 통합 프로젝트

[`Field Notes`](exercises/field-notes/)는 기록, 사진과 선택적 위치를 기기에 저장하고 나중에 서버와 동기화하는 완성된 애플리케이션입니다.

```sh
cd exercises/field-notes
npm install
npm run verify
```

문서를 전부 읽은 뒤 프로젝트를 시작하지 않습니다.

```text
runtime·layout·navigation
→ 기본 화면과 상태 형식 확인
→ SQLite·outbox
→ 카메라·사진·위치 권한
→ 실패 재현 서버와 동기화
→ 백그라운드 작업과 알림
→ 네이티브 빌드·테스트·릴리스 근거
→ 실제 Android·iOS 기기 확인
```

## 다른 트랙과의 연결

### 웹에서 모바일로 이동

다음 능력이 있으면 시작할 수 있습니다.

- 외부 JSON을 검사하고 내부 타입으로 변환합니다.
- React 상태와 비동기 요청 수명을 다룹니다.
- 세션 만료와 오류 응답을 구분합니다.

브라우저의 URL, storage와 수명 규칙을 그대로 모바일에 적용하지 않습니다. 앱 프로세스, SQLite, 운영체제 권한과 설치된 바이너리의 수명을 새로 구분합니다.

### 백엔드와 연결

오프라인 동기화는 서버가 다음을 제공한다는 전제가 필요합니다.

- 안정적인 record ID와 version
- 중복 요청 처리 기준
- 인증 만료와 권한 오류 구분
- 충돌 결과와 재시도 가능 여부

서버 측 계약은 웹·백엔드와 distributed-services에서 다룹니다.

### 네이티브 전문 개발로 이동

Kotlin 또는 Swift로 플랫폼 전용 기능을 깊게 구현해야 하면 이 과정 완료 뒤 별도 네이티브 언어·플랫폼 과정으로 이동합니다. React Native 전체를 마친 뒤 두 네이티브 플랫폼을 모두 선행 학습하지 않습니다.

## 검증 한계

자동 검사는 실제 권한 대화 상자, 카메라·위치 제공자, 운영체제의 백그라운드 실행, 실제 push 전달, 서명 인증 정보와 스토어 검토를 대신하지 않습니다. 확인하지 못한 항목은 `미검사`로 기록합니다.

## 완료 기준

- 필수 문서의 상태 소유자, 상태를 바꾸는 사건과 실패 뒤 남아야 하는 값을 설명합니다.
- `Field Notes`의 타입 검사와 테스트를 통과합니다.
- 프로세스 종료, DB migration, 오프라인 저장, 응답 유실, 중복 요청, 충돌과 권한 거절·철회를 재현합니다.
- Android와 iOS 개발용 빌드에서 핵심 작업을 확인합니다.
- 실제 산출물과 소스, 앱 버전, 빌드 번호와 runtimeVersion을 연결합니다.
- 확인하지 않은 플랫폼·기기·서명·스토어 범위를 명시합니다.

## 범위 밖

Kotlin·Swift 전체, 네이티브 전문 개발, push 제공자와 백엔드 운영, 스토어 사업 운영을 대신하지 않습니다.
