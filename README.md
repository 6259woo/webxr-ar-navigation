# WebXR AR Navigation Prototype

> **2025년 1학기 SW캡스톤디자인 (팀: 혼자서도 뚜벅뚜벅)**<br>
WebXR 기술을 활용하여 별도의 앱 설치 없이 모바일 크롬(안드로이드)에서 실행 가능한 증강현실(AR) 실내 내비게이션 시스템입니다.


## 프로젝트 Demo
AR을 이용한 직관적인 길 안내와 효율적인 맵 제작 툴을 제공합니다.

<!-- ![Demo Video1](./demo/demo_web.mp4)<br> -->
<!-- <video src="./demo/demo_web.mp4" controls width="100%"></video> -->
[![Web Demo](https://img.youtube.com/vi/H0PALPWTd6Q/0.jpg)](https://www.youtube.com/watch?v=H0PALPWTd6Q)<br>
(이미지를 클릭하면 유튜브 시연 영상으로 이동합니다)<br>
AR을 이용해 보다 직관적인 길 안내가 가능합니다.

<!-- ![Demo Video2](./demo/캡스톤_시연_툴.mp4)<br> -->
<!-- <video src="./demo/demo_tool.mp4" controls width="100%"></video> -->
[![Web Demo](https://img.youtube.com/vi/GhW_MLR3vos/0.jpg)](https://www.youtube.com/watch?v=GhW_MLR3vos)<br>
(이미지를 클릭하면 유튜브 시연 영상으로 이동합니다)<br>
2D도면을 이용한 graph map작성 툴의 시연 영상입니다.

## Key Features
* **Web-based AR**: 별도의 앱 설치 없이 URL 접속만으로 AR 기능 구현 (WebXR API)
* **Marker-based Tracking**: 이미지 트래킹을 통한 초기 위치 세팅 및 좌표계 변환
* **Hybrid Navigation**: AR 시각화 경로(스플라인 곡선)와 미니맵을 동시 제공하여 직관적인 안내 제공
* **Custom Map Tool**: 2D 도면을 기반으로 노드와 엣지를 생성하는 그래프 기반 맵 데이터 구조화 툴 개발
* **Error Compensation**: WebXR API의 SLAM 기반 Visual Odometry에서 발생하는 오차를 자동 보상하는 알고리즘 적용

## Tech Stack
- **Frontend**: WebXR, Three.js, GLTFLoader (3D 모델링 처리)
- **Backend**: Node.js, Express
- **Network**: ngrok (HTTPS 터널링)
- **Data**: Matplotlib (맵 데이터 전처리), JSON (그래프 구조), OpenCV (Map Tool 개발에 사용)

## Installation & Setup
### 1. Server Side (Node.js)
본 프로젝트는 외부 접속 및 보안 권한을 위해 HTTPS 환경이 필수입니다.

```bash
# 의존성 설치
npm install

# 서버 실행
node server.js
```

**Trouble Shooting (EACCES 에러 발생 시)**


실행 권한 문제 해결: `chmod +x "./node_modules/ngrok/bin/ngrok"`

또는 패키지 재설치: `rm -rf node_modules/ngrok && npm install ngrok`

---
### 2. Client Side (Android Mobile Chrome)
**주의: iOS는 현재 지원되지 않으며, 안드로이드 전용 기능입니다.**

1. Chrome Flags 설정: 최신 WebXR 기능을 위해 아래 주소를 주소창에 입력 후 **Enabled**로 변경하세요.
    * `chrome://flags/#webxr-incubations` (WebXR Incubations 활성화)

2. **HTTPS 접속**: 서버 실행 시 터미널에 표시된 **ngrok 주소**를 통해 접속해야 카메라 권한 사용이 가능합니다.

3. **권한 허용**: 브라우저에서 요청하는 '카메라' 및 'AR' 권한을 반드시 허용해 주세요.
---
## How to Use
1. **서버 구동**: `node server.js` 명령어로 서버를 실행합니다.

2. **접속**: 스마트폰 크롬 브라우저에서 ngrok 주소로 접속합니다.

3. **목적지 입력**: 검색창에 목적지(예: 1362, 1319, 3F 엘리베이터 입구 등)를 입력합니다.

4. **위치 초기화**: '마커인식' 버튼을 누르고 지정된 마커(./public/test.png)를 스캔합니다.

5. **안내 시작**: 설정된 출발지로부터 목적지까지 생성된 AR 가이드를 따라 이동합니다.

---

## ⚠️ Notice
* **대상 공간**: 한림대학교 공학관 3층만 지원 (해당 도면 기반으로 제작됨)

* **출발 위치**: 프로토타입인 관계로 시작위치는 한림대 공학관 1340(신범주 교수님 연구실)로 지정되어 있습니다. 연구실 문앞 마커를 인식시켜 위치를 세팅하는 시나리오 입니다.

* **개발 방식**: 본 프로젝트는 신기술 경험 위해 AI 코딩 보조 도구를 적극 활용하였습니다.

---

## Team 혼자서도 뚜벅뚜벅
**이정우**: [좌표계변환 로직 구현, AR세션 보조 및 3D모델링, Map 데이터 구축]

**김채연**: [클라이언트 및 WebXR AR세션]

**한유빈**: [서버 및 보고서 정리]

## 최종 시연 영상
<!-- ![Demo Video3](./demo/2025-1캡스톤디자인시연영상.mp4) -->
<!-- <video src="./demo/demo_final.mp4" controls width="100%"></video> -->
(이미지를 클릭하면 유튜브 시연 영상으로 이동합니다)<br>
[![Web Demo](https://img.youtube.com/vi/eesUiA88n3M/0.jpg)](https://www.youtube.com/watch?v=eesUiA88n3M)<br>