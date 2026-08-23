# 컴퓨터 네트워크 기초

이 브랜치는 링크 전달부터 응용 프로토콜까지 한 요청이 지나가는 과정을 문서와 실행 가능한 프로젝트로 검증합니다. 명령을 외우는 대신 패킷 필드, 경로 선택, TCP 상태, 손실 복구와 진단 결과가 어떤 입력에서 나오는지 확인합니다.

별도의 외부 프로젝트 없이 필수 과정을 완료할 수 있습니다. 다른 개발 트랙에서는 필요한 계층만 선택해 사용할 수 있습니다.

## 대상 독자와 선행 지식

- 2진수와 16진수 표기를 읽습니다.
- 작은 Python 프로그램과 단위 테스트를 실행합니다.
- 명령행에서 파일과 프로세스를 다룹니다.

Linux 네트워크 실험에는 관리자 권한이 필요합니다. 운영 장비가 아니라 폐기 가능한 VM이나 격리된 환경에서만 실행합니다.

## 완료 후 갖춰야 할 능력

- 애플리케이션 데이터가 Ethernet 프레임까지 캡슐화되는 과정을 설명합니다.
- MAC, VLAN, ARP와 IPv6 Neighbor Discovery의 적용 범위를 구분합니다.
- CIDR 프리픽스를 계산하고 최장 프리픽스 일치로 경로를 선택합니다.
- IP 전달, TTL/Hop Limit, MTU, ICMP, NAT, 연결 추적과 방화벽 판정을 구분합니다.
- 라우팅 데이터 평면과 제어 평면을 구분합니다.
- UDP 데이터그램과 TCP 바이트 스트림의 차이를 바탕으로 메시지 구분과 손실 처리 주체를 정합니다.
- TCP 연결 상태, 순서 번호, ACK, RTT, RTO, `rwnd`와 `cwnd`를 설명합니다.
- DNS부터 HTTP까지 마지막 성공 단계와 첫 실패 단계를 관찰 자료로 좁힙니다.

## 저장소 구성

```text
.
├── README.md
├── docs/
├── examples/
│   └── window-model/
└── exercises/
    ├── protocol-inspector/
    ├── linux-routing-nat/
    ├── path-diagnosis/
    └── tcpdump-analyzer/
```

## 정본 전체 과정

### 1. 링크와 종단 경로

- [계층, 캡슐화와 종단 경로](docs/01-link-and-path/01-layers-encapsulation-and-path.md)
- [Ethernet, MAC 주소와 스위칭](docs/01-link-and-path/02-ethernet-mac-and-switching.md)
- [ARP와 IPv6 Neighbor Discovery](docs/01-link-and-path/03-arp-and-neighbor-discovery.md)

### 2. 인터넷 계층과 경로

- [IP 주소, 서브넷과 라우팅 조회](docs/02-internetworking/01-ip-addressing-subnets-and-lpm.md)
- [IP 전달, MTU와 ICMP](docs/02-internetworking/02-ip-forwarding-mtu-and-icmp.md)
- [NAT, 연결 추적과 방화벽](docs/02-internetworking/03-nat-connection-tracking-and-firewalls.md)
- [라우팅 알고리즘과 프로토콜](docs/02-internetworking/04-routing-algorithms-and-protocols.md)

### 3. 전송 계층

- [UDP와 TCP의 서비스 특성](docs/03-transport/01-udp-and-tcp-service-contracts.md)
- [TCP 연결 상태와 순서 번호](docs/03-transport/02-tcp-connection-state-and-sequences.md)
- [재전송, RTT와 슬라이딩 윈도](docs/03-transport/03-retransmission-rtt-and-sliding-windows.md)
- [흐름 제어와 혼잡 제어](docs/03-transport/04-flow-and-congestion-control.md)

### 4. 응용 연결과 장애 진단

- [DNS, HTTP, TLS와 QUIC](docs/04-application-security-and-evidence/01-dns-http-tls-and-quic.md)
- [단계별 네트워크 장애 진단](docs/04-application-security-and-evidence/02-network-failure-localization.md)

## 필수 프로젝트

### [`protocol-inspector`](exercises/protocol-inspector/)

체크섬, Ethernet·IPv4·TCP 파싱, classic PCAP, 최장 프리픽스 일치와 제한된 TCP 상태 기계를 고정 입력으로 검증합니다.

### [`linux-routing-nat`](exercises/linux-routing-nat/)

격리된 Linux 환경에서 IPv4 전달, TTL 만료, 경로 제거·복구, SNAT, 초기 SYN 손실과 재전송을 재현합니다.

### [`path-diagnosis`](exercises/path-diagnosis/)

DNS부터 HTTP까지의 관찰 결과를 읽고 마지막 성공 단계, 첫 실패 단계, 진단 코드와 종료 상태를 판정합니다.

## 다른 개발 트랙에서 사용하는 방법

### 웹 개발

다음을 우선 사용합니다.

- IP 주소와 포트의 기본 구분
- TCP 서비스 특성
- DNS, TLS와 HTTP
- 단계별 장애 진단

Ethernet, 라우팅 프로토콜, 혼잡 제어 계산과 NAT 내부 실험은 장애 원인을 더 낮은 계층에서 조사해야 할 때 확장합니다.

### C/C++ 네트워크 프로그램

다음을 권장합니다.

- UDP/TCP 서비스 특성과 TCP 상태
- 부분 읽기와 메시지 구분에 필요한 전송 모델
- 체크섬·패킷 구조와 PCAP 분석
- 재전송, 흐름·혼잡 제어
- 단계별 장애 진단

소켓 API와 파일 디스크립터 수명은 `c` 또는 `cpp` 브랜치에서 함께 학습합니다.

### 게임 서버

다음을 우선 사용합니다.

- UDP와 TCP의 차이
- 순서 번호, 중복, 손실과 재전송
- RTT, RTO, 흐름·혼잡 제어
- NAT와 연결 추적
- 패킷 캡처와 장애 진단

게임 명령 순서, 서버 권위 상태, snapshot과 재접속은 game-server 브랜치가 소유합니다.

## 선택 자료

- [컴퓨터 네트워크 표준 지도](docs/90-standards-map.md)
- [송신 창 모델](examples/window-model/README.md)
- [tcpdump 분석기](exercises/tcpdump-analyzer/README.md)

## 실행과 안전

```sh
cd exercises/protocol-inspector
python3 -m unittest discover -s tests -v

cd ../path-diagnosis
python3 -m unittest discover -s tests -v
```

Linux 실험은 사전 검사를 통과한 격리 환경에서 실행합니다.

```sh
cd exercises/linux-routing-nat
sudo ./scripts/preflight.sh all
sudo ./scripts/run-all.sh
```

## 완료 기준

- 필수 문서의 핵심 질문에 답합니다.
- `protocol-inspector`와 `path-diagnosis`의 검사를 통과합니다.
- 격리된 Linux 환경에서 라우팅, NAT와 손실 실험을 통과합니다.
- 패킷 파서 결과와 실제 캡처의 관찰 범위를 구분합니다.
- 임의의 연결 실패에서 관찰 위치, 마지막 성공 단계, 첫 실패 단계와 다음 읽기 전용 검사를 기록합니다.

## 범위 밖

특정 네트워크 장비 운영, 대규모 라우팅 정책, production 방화벽 변경, 고성능 packet processing과 완전한 QUIC 구현은 포함하지 않습니다. 표준과 구현 세부가 중요하면 현재 RFC와 실제 구현 문서를 다시 확인합니다.
