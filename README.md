# SW 경진대회 출품작(Forestore)

> 마트 재고량 데이터 mocking용 프로젝트

### [서비스 소개](https://github.com/hou27/mju_mart_visualize/blob/main/README.md)

## 1. 개요

- 마트 재고량 데이터를 mocking 하기 위한 프로젝트입니다.

## 2. 프로젝트 구조

### init.py

> 첫번째 재고량 감소 사이클을 생성

### decrease_stock.py

> 재고량 감소 이벤트를 생성

### generate_special_event.py

> 특별 이벤트를 생성(큰 폭의 재고량 감소)

### detect_trend.py

> 다음 재고량 감소 사이클을 생성을 위해 재고량 감소 추세를 계산

### add_cycle.py

> 재고량 감소 사이클 하나를 추가

### generate_excel.py

> 데이터프레임을 엑셀 파일로 생성

## 3. 프로젝트 실행 방법

### 3.1. 필요 라이브러리 설치

```
pip install -r requirements.txt
```

### 3.2. 프로젝트 실행

```
python main.py

# 또는 재고량 감소 사이클을 몇 개 생성할지 인자로 전달
python main.py 12
```
