# Sewer Observation System

원티드 5차 백엔드 프리온보딩 코스 4차 과제

- [Sewer Observation System](#sewer-observation-system)
  - [앱 소개](#앱-소개)
    - [data](#data)
  - [API Doc](#api-doc)
  - [Open API](#open-api)

## 앱 소개

### data
- `Gu`: 구 정보 모델
  - `name`: 구 이름
  - `code`: 구 코드 (강우계 데이터에서 사용)
  - `gubn`: 구분 코드 (하수관로 데이터에서 사용)
- `Sewer`: 서울시 하수관로 정보 데이터 
  - `idn`: 고유번호
  - `gu`: 구 외래키
  - `remark`: 위치정보
- `Sewage`: 시간 별 하수관로 수위 정보 데이터
  - `sewer`: 하수관로 ID
  - `mea_ymd`: 측정일자
  - `mea_wal`: 측정수위
  - `sig_sta`: 통신상태
- `Rainguage`: 서울시 강우계 정보 데이터
  - `gu`: 구 외래키
  - `rainguage_code`: 강우량계 코드
  - `rainguage_name`: 강우량계명
- `Rainfall`: 시간 별 강우계 강수량 정보 데이터
  - `rainguage`: 강우량계 ID
  - `rainfall10`: 10분우량
  - `recieve_time`: 자료수집 시각

## API Doc

|Method|Path|Description|
|------|----|-----------|
|GET|/api/v1/gu/|실시간 강수량, 하수관 데이터를 응답|

## Open API

- 서울시 하수관로 수위 정보 API: https://data.seoul.go.kr/dataList/OA-2527/S/1/datasetView.do
- 서울시 강우량 정보 API: https://data.seoul.go.kr/dataList/OA-1168/S/1/datasetView.do
