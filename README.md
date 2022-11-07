# Sewer Observation System

원티드 5차 백엔드 프리온보딩 코스 4차 과제

## 목차
- [Sewer Observation System](#sewer-observation-system)
  - [목차](#목차)
  - [앱 소개](#앱-소개)
    - [data](#data)
  - [Open API](#open-api)

## 앱 소개

### data

- `Sewer`: 서울시 하수관로 정보 데이터 
  - `idn`: 고유번호
  - `gubn`: 구분코드
  - `gubn_nam`: 구분명
  - `remark`: 위치정보
- `Sewage`: 시간 별 하수관로 수위 정보 데이터
  - `sewer`: 하수관로 ID
  - `mea_ymd`: 측정일자
  - `mea_wal`: 측정수위
  - `sig_sta`: 통신상태
- `Rainguage`: 서울시 강수량 정보 데이터
  - `rainguage_code`: 강우량계 코드
  - `rainguage_name`: 강우량계명
  - `gu_code`: 구청 코드
  - `gu_name`: 구청명
- `Rainfall`: 시간 별 강우계 강수량 정보 데이터
  - `rainguage`: 강우량계 ID
  - `rainfall10`: 10분우량
  - `recieve_time`: 자료수집 시각

## Open API

- 서울시 하수관로 수위 정보 API: https://data.seoul.go.kr/dataList/OA-2527/S/1/datasetView.do
- 서울시 강우량 정보 API: https://data.seoul.go.kr/dataList/OA-1168/S/1/datasetView.do
