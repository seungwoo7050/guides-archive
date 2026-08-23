# React·Next.js 실전 개발 가이드

이 저장소는 React와 Next.js 문법을 처음 배우는 입문서가 아닙니다. TypeScript와 React로 작은 기능을 구현해 본 개발자가 실제 프로젝트에 들어가 코드를 읽고, 기능을 완성하고, 운영 환경에서 확인하는 데 필요한 판단 기준을 다룹니다.

실제 프로젝트는 이 저장소 밖에서 진행합니다. `docs/`에는 프로젝트 진입 전에 읽을 최소 문서와 구현 중 찾아볼 자료가 있으며, `exercises/`에는 실제 프로젝트를 통과한 뒤 가이드 없이 역량을 확인할 완성된 프로그램이 있습니다.

## 학습 순서

```text
Stable Core Guide
→ Actual Project
→ JIT Guide as needed
→ Project PASS
→ Competency Suite without Guide
→ Rewind where needed
```

## 1. Stable Core Guide

프로젝트 종류와 관계없이 먼저 읽을 문서는 두 개입니다.

1. [`프로젝트 합류`](docs/01-project-onboarding.md)
   - Node.js, package manager, lock file, build와 test 명령을 확인합니다.
   - Server Component, Client Component와 Route Handler가 어디에서 실행되는지 구분합니다.
   - 처음 보는 저장소에서 URL 하나가 어떤 파일과 요청을 거쳐 화면에 나타나는지 추적합니다.
2. [`UI와 상태`](docs/02-ui-and-state-architecture.md)
   - URL 상태, server 상태, 화면 상태, 입력 초안과 계산값을 구분합니다.
   - 외부 입력을 `unknown`으로 받고 검사한 뒤 내부 타입으로 변환합니다.
   - 값을 어느 component가 저장하고 어떤 event가 바꿀지 정합니다.

이 두 문서는 commerce, portfolio, realtime과 collaboration 등 대상 프로젝트가 달라져도 그대로 유지합니다.

## 2. Actual Project

Stable Core를 읽은 뒤 실제 프로젝트 구현을 시작합니다. 이 저장소의 exercise를 먼저 수행하지 않습니다.

프로젝트에 들어가면 다음 항목부터 확인합니다.

- 설치, 개발 server, typecheck, test, build와 production start 명령
- 사용자 행동 하나가 통과하는 URL, server code, client code와 HTTP 요청
- 외부 입력을 검사하는 위치
- URL, server 응답과 입력 초안을 저장하는 위치
- 실패해도 유지해야 할 마지막 정상 결과와 사용자 입력

## 3. JIT / Rewind Guide

구현이 해당 문제에 도달했을 때만 읽습니다.

- [`Next.js data, Effect와 동시 실행`](docs/03-nextjs-data-effects-and-concurrency.md)
  - URL과 history, Effect 정리, 요청 취소, 늦은 응답 차단, 낙관적 갱신과 version conflict
- [`test, 접근성과 성능`](docs/04-testing-accessibility-and-performance.md)
  - test 위치, browser E2E, keyboard와 focus, 좁은 화면, motion 감소와 성능 예산
- [`production runtime`](docs/05-production-runtime-contract.md)
  - production build와 start, health 응답, release 식별자, secret 노출 검사와 smoke test
- [`실무 점검표`](docs/90-practical-checklist.md)
  - 구현, review, 장애 분석과 Rewind 범위를 정할 때 필요한 항목

## 4. Competency Suite

필수 역량 검증 프로그램은 [`project-catalog`](exercises/project-catalog/)입니다.

- URL query 정규화와 server 첫 render
- `unknown` JSON 검사
- 서로 모순되지 않는 화면 상태
- 요청 취소와 generation 확인
- 낙관적 변경과 `409 Conflict` 복구
- keyboard 조작과 focus 이동
- Route Handler의 입력·응답 처리
- 단위, browser와 production smoke test

실제 프로젝트가 PASS한 뒤 README와 test를 확인하고 가이드를 다시 읽지 않은 상태에서 구현합니다.

```text
PASS
→ 역량 확인 완료

FAIL
→ 실패한 영역의 Guide만 다시 읽기
→ 같은 검증 다시 실행
```

## 선행 지식

- 의미에 맞는 HTML 요소와 form label
- CSS 기본 배치, Flexbox와 Grid
- JavaScript module, Promise, `async`와 `await`
- TypeScript union, `unknown`과 narrowing
- React props, state, event, Effect와 정리 함수
- Next.js App Router의 `page.tsx`, `layout.tsx`와 Route Handler
- HTTP method, status, header와 JSON body
- Node.js, `package.json`, script와 lock file

위 항목이 낯설다면 `web-application`에서 먼저 보완합니다.

## 저장소 구성

```text
.
├── README.md
├── docs/
│   ├── 00-roadmap.md
│   ├── 01-project-onboarding.md
│   ├── 02-ui-and-state-architecture.md
│   ├── 03-nextjs-data-effects-and-concurrency.md
│   ├── 04-testing-accessibility-and-performance.md
│   ├── 05-production-runtime-contract.md
│   └── 90-practical-checklist.md
└── exercises/
    └── project-catalog/
```

## 완료 기준

- Stable Core를 읽고 처음 보는 React·Next.js 프로젝트의 실행 방법과 주요 파일을 확인합니다.
- 실제 프로젝트에서 사용자 기능 하나를 production build와 실제 browser 동작까지 확인합니다.
- 필요한 JIT 문서만 골라 적용합니다.
- `project-catalog`의 전체 검증을 가이드 없이 통과합니다.
- 실패한 영역이 있었다면 관련 문서만 다시 읽고 같은 검증을 통과합니다.
