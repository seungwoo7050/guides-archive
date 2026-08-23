# 웹 인프라 가이드

이 브랜치는 웹 요청이 서버 프로세스에 도착하고, Docker Compose 안에서 Nginx, PHP-FPM과 MariaDB가 함께 동작하는 과정을 실제 프로젝트에서 구현하기 위한 최소 기반과 JIT 문서를 제공합니다.

```text
Stable Core
→ Actual Project
→ 서비스별 JIT Guide
→ Project PASS
→ 장애 진단으로 경험 정리
→ notes-stack을 가이드 없이 재구현
→ 실패한 부분만 Rewind
```

실제 공인 도메인과 장기 운영 환경을 준비하는 과정은 의도적으로 필수 범위에서 제외합니다.

## 대상 프로젝트

대표 적용 대상은 Docker Compose로 Nginx, 애플리케이션 runtime과 관계형 데이터베이스를 구성하는 프로젝트입니다. 현재 프로젝트 모음에서는 `web/inception`과 같은 과제에 사용할 수 있습니다.

## Stable Core

프로젝트에 들어가기 전에 다음 세 문서를 읽습니다.

1. [`웹 요청과 서버`](docs/01-foundations/01-web-request-and-server.md)
2. [`Docker 이미지와 컨테이너`](docs/01-foundations/02-docker-image-and-container.md)
3. [`Compose, 네트워크와 저장소`](docs/01-foundations/03-compose-network-and-storage.md)

다음 질문에 답할 수 있어야 합니다.

- 요청이 어느 주소와 포트로 들어옵니까?
- 컨테이너 안에서 어떤 프로세스가 PID 1로 실행됩니까?
- 서비스끼리 어떤 이름과 내부 포트로 연결됩니까?
- 컨테이너를 다시 만들어도 남아야 하는 데이터는 어디에 저장합니까?

## 프로젝트 진입 기준

- host port와 container port를 구분합니다.
- image, container와 volume의 수명을 설명합니다.
- foreground process와 PID 1의 종료 신호를 설명합니다.
- Compose service name을 내부 DNS 이름으로 사용합니다.
- 비밀값을 image나 source에 굽지 않아야 하는 이유를 설명합니다.
- 하나의 서비스를 시작·중지하고 log와 종료 상태를 확인합니다.

## Actual Project에서 먼저 할 일

1. 공개 port, 내부 service와 volume 목록을 작성합니다.
2. 각 container의 PID 1과 준비 조건을 정합니다.
3. 빈 volume과 기존 volume에서 시작 결과를 구분합니다.
4. Nginx에서 애플리케이션까지 가장 작은 요청 경로를 먼저 연결합니다.
5. 데이터베이스를 추가하고 초기화가 반복 실행돼도 중복되지 않게 만듭니다.
6. 잘못된 host, password, port와 secret path를 하나씩 주입해 첫 실패를 기록합니다.

## JIT / Rewind 지도

| 구현하거나 조사할 내용 | 문서 |
|---|---|
| HTTPS gateway와 FastCGI | [`Nginx, TLS와 PHP-FPM`](docs/02-service-stack/04-nginx-tls-and-php-fpm.md) |
| DB 최초 초기화와 기존 volume | [`데이터베이스 생명주기`](docs/02-service-stack/05-database-lifecycle.md) |
| 반복 가능한 schema·초기 데이터 | [`애플리케이션 초기화`](docs/02-service-stack/06-idempotent-app-bootstrap.md) |
| 404·500·502·DB 인증·복구 | [`운영, 장애 진단과 복구`](docs/02-service-stack/07-operations-debugging-and-recovery.md) |

4~6장은 해당 서비스를 구현할 때 읽습니다. 7장은 구현 중 장애를 충분히 경험했거나 프로젝트 완료 뒤 읽습니다.

## Project PASS 기준

- 빈 환경에서 전체 stack을 시작합니다.
- container 재생성 뒤 volume 데이터가 보존됩니다.
- Nginx, PHP-FPM과 MariaDB가 필요한 내부 port만 사용합니다.
- 비밀값이 image layer와 일반 log에 노출되지 않습니다.
- DB 초기화와 seed가 반복 실행돼도 중복되지 않습니다.
- 잘못된 host, password, secret path와 FastCGI port를 구분해 진단합니다.
- 논리 backup을 만들고 빈 환경에 restore합니다.
- 종료 시 child process가 고아로 남지 않습니다.

로컬 TLS, Compose와 합성 장애 검증을 통과해도 공인 인증서, 외부 DNS와 실제 운영 장애를 검증한 것은 아닙니다.

## Competency Suite

[`notes-stack`](exercises/notes-stack/README.md)은 Nginx, PHP-FPM과 MariaDB를 별도 container로 실행하는 작은 메모 서비스입니다.

- 빈 DB volume에서만 실행되는 초기화
- 내부 network에서만 접근 가능한 DB와 PHP-FPM
- 로컬 TLS와 FastCGI 전달
- 파일로 주입한 password와 tmpfs 사본
- 횟수를 제한한 DB 연결 재시도
- 반복 가능한 schema와 초기 데이터
- volume 보존
- 논리 backup과 restore
- 잘못된 설정과 상태 검사 재현

실제 프로젝트를 PASS한 뒤 이전 구현과 가이드를 보지 않고 다시 구성합니다.

## FAIL → Rewind

- `curl`, container 상태, process log와 DB 상태에서 마지막 성공 단계를 찾습니다.
- 2차 증상보다 첫 실패를 먼저 수정합니다.
- 같은 잘못된 설정을 재현하는 검사를 남깁니다.
- 관련 문서만 다시 읽고 전체 stack을 빈 환경에서 재검증합니다.

## 완료 기준

- Stable Core 뒤 실제 Compose 프로젝트를 시작하고 PASS합니다.
- 필요한 서비스 문서만 JIT로 적용합니다.
- `notes-stack`을 가이드와 이전 구현 없이 다시 구성합니다.
- backup 파일을 실제로 restore해 결과를 확인합니다.
- 공인 DNS·TLS, CI/CD와 장기 운영을 검사하지 않았음을 명시합니다.

## 의도적으로 제외한 운영 범위

- Kubernetes와 다중 host orchestration
- 고가용성 DB와 자동 failover
- 공인 인증서 자동 갱신
- CI/CD와 image registry 운영
- 대규모 관측 시스템
- 조직 단위 secret 관리와 보안 감사

이 항목들은 로컬에서 결정적으로 재현하기 어렵고 계정, 비용, 외부 DNS와 장시간 관찰이 필요합니다. 본 과정 완료를 실제 production 운영 경험으로 표현하지 않습니다.
