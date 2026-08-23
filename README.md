# 웹 애플리케이션 개발 가이드

이 브랜치는 작은 풀스택 웹 애플리케이션을 실제 프로젝트에서 구현하기 위한 공통 기반, 기능별 JIT 문서와 프로젝트 완료 뒤 전이 검증을 제공합니다. 모든 문서를 먼저 읽고 exercise를 끝낸 뒤 프로젝트에 들어가지 않습니다.

```text
Stable Core
→ Actual Project
→ 필요한 주제를 JIT로 확인
→ Project PASS
→ Competency Suite without Guide
→ 실패한 주제만 Rewind
```

## 대상 프로젝트

브라우저 UI, HTTP API, 관계형 데이터, 인증과 선택적인 실시간 통신을 한 프로젝트에서 연결하는 웹 애플리케이션을 대상으로 합니다. 현재 프로젝트 모음에서는 `web/ft_transcendence`와 같은 풀스택 프로젝트에 적용할 수 있습니다.

## 저장소 구성

```text
.
├── README.md
├── docs/
│   ├── 01-web-foundations/
│   ├── 02-frontend/
│   ├── 03-backend/
│   ├── 04-data-and-security/
│   └── 05-realtime-and-quality/
└── exercises/
    ├── browser-directory/
    ├── runtime-workspace/
    ├── user-directory/
    ├── notes-api/
    ├── seat-reservation/
    ├── session-access-control/
    └── realtime-board/
```

## Stable Core

프로젝트 진입 전에는 다음 실행 원리와 구현 기준을 익힙니다.

- HTTP 요청과 응답, browser와 Node.js의 실행 위치
- JavaScript module, Promise와 실패 처리
- TypeScript 타입과 실행 시 외부 입력 검증의 차이
- DOM, form과 기본 접근성
- React 상태, event와 Effect 수명
- Next.js의 Server Component, Client Component와 Route Handler
- HTTP route, 업무 처리와 저장 코드의 분리
- Fastify application 생성과 실제 port 열기의 분리

세부 문서는 [`docs/00-roadmap.md`](docs/00-roadmap.md)에서 Core와 JIT로 구분합니다.

## 프로젝트 진입 기준

다음 질문에 답할 수 있으면 실제 프로젝트를 시작합니다.

- browser와 Node.js에서 코드가 각각 어디서 실행됩니까?
- Promise 실패와 HTTP 오류 응답은 어떻게 다릅니까?
- TypeScript 타입만으로 외부 입력을 신뢰하면 안 되는 이유는 무엇입니까?
- React 상태와 Effect를 어느 component에 둘지 어떻게 정합니까?
- Server Component와 Client Component를 어떻게 구분합니까?
- route, 업무 규칙과 저장 코드를 어떻게 나눕니까?
- application 생성과 network listen을 왜 분리합니까?

데이터베이스, 인증과 WebSocket을 미리 완벽하게 공부하려고 프로젝트 시작을 늦추지 않습니다.

## Actual Project에서 먼저 할 일

1. 설치, 개발 server, typecheck, test, build와 production start 명령을 확인합니다.
2. 사용자 행동 하나가 URL, server code, client code와 HTTP 요청을 거치는 경로를 추적합니다.
3. 외부 입력을 검사하는 위치를 찾습니다.
4. URL, server 응답, 화면 상태와 입력 초안을 누가 보관하는지 정합니다.
5. 실패해도 유지해야 할 마지막 정상 결과와 사용자 입력을 정합니다.
6. 하나의 작은 수직 기능을 정상·오류·새로고침까지 완성합니다.

## JIT / Rewind 지도

| 구현할 내용 | 문서 영역 |
|---|---|
| browser URL, DOM, 비동기와 TypeScript | [`01-web-foundations`](docs/01-web-foundations/) |
| React 상태, form, Effect와 Next.js | [`02-frontend`](docs/02-frontend/) |
| HTTP API, Fastify와 runtime validation | [`03-backend`](docs/03-backend/) |
| PostgreSQL, transaction, session, 권한, CSRF·CORS | [`04-data-and-security`](docs/04-data-and-security/) |
| WebSocket, 상태 복구, Canvas와 test | [`05-realtime-and-quality`](docs/05-realtime-and-quality/) |

프로젝트 구현 중에는 JIT 자료로, Competency Suite에서 실패한 뒤에는 Rewind 자료로 사용합니다.

## Project PASS 기준

- 사용자 기능 하나가 실제 browser에서 처음부터 끝까지 동작합니다.
- 외부 입력을 runtime에서 검사합니다.
- 오류 응답과 network 실패를 구분해 화면에 반영합니다.
- schema 제약과 transaction으로 경쟁 쓰기 또는 rollback 조건을 확인합니다.
- 인증 정보 발급·폐기, 객체 소유권과 역할 권한을 검사합니다.
- 실시간 기능이 있다면 reconnect, version conflict와 resource cleanup을 확인합니다.
- 단위, API와 browser 검사를 목적에 맞게 나눕니다.
- 고정 설치, production build와 production start를 확인합니다.
- 운영 host, 공인 DNS·TLS와 backup을 검사하지 않았다면 미검사로 기록합니다.

## Competency Suite

실제 프로젝트를 PASS한 뒤 다음 프로젝트 중 필요한 검증을 가이드와 기존 구현 없이 수행합니다.

| 프로젝트 | 다시 확인하는 능력 |
|---|---|
| `browser-directory` | URL과 history로 browser 상태 복원 |
| `runtime-workspace` | Node.js 실행 환경, TypeScript 입력 검증과 package 경계 |
| `user-directory` | React 상태, 비동기 요청 수명과 Next.js route |
| `notes-api` | 요청 검증, 업무 처리, 저장 코드와 HTTP 오류 분리 |
| `seat-reservation` | 제약과 transaction으로 경쟁 쓰기·rollback 처리 |
| `session-access-control` | session 수명, Origin, 객체 소유권과 역할 권한 |
| `realtime-board` | WebSocket, 방 참가, version conflict, snapshot 복구와 정리 |

각 프로젝트는 해당 디렉터리만 복사해 설치하고 테스트할 수 있어야 합니다.

## FAIL → Rewind

1. exercise의 README, 공개 API와 test failure를 읽습니다.
2. 기존 구현과 가이드를 보기 전에 자신의 요구사항 해석과 상태 배치를 확인합니다.
3. 원인을 설명하지 못하는 주제만 다시 읽습니다.
4. 같은 실패를 검출하는 test를 남기고 전체 검사를 다시 실행합니다.

## 완료 기준

- Stable Core 뒤 실제 풀스택 프로젝트를 시작해 PASS합니다.
- 프로젝트에 필요한 JIT 문서만 선택합니다.
- 선택한 Competency Suite를 가이드 없이 통과합니다.
- 상태를 누가 보관하고 실패 뒤 어떤 값이 남는지 설명합니다.
- 자동 검사와 실제 배포·운영 경험의 차이를 명시합니다.

## 범위 밖

운영 host, 공인 DNS·TLS, 배포 자동화, 중앙 관측, backup·복구, DBMS 저장 엔진, 서비스 사이 Saga와 특정 산업 규제는 별도 과정과 실제 업무가 맡습니다.
