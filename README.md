# NIADataAccuracyTools

[![N|Solid](http://www.sweetk.co.kr/wp-content/uploads/2017/09/LOGO_L-e1504836363975.png)](http://www.sweetk.co.kr/)

사람 인체자세 3D AI 데이터 유효성 및 정확성 검사 툴

[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)

## Introduction
2020 정보화 진흥원 인공지능 학습용 데이터 구축사업 수행을 위한 인공지능 데이터 정확성 검사 모듈입니다

## Installation
저장소 클론
```shell script
git clone https://github.com/kwonhyeokmin/NIADataAccuracyTools.git
```
필요 패키지 설치
```shell script
pip install -r requirements.txt
```
검증 모듈 실행
```shell script
python main.py --[yaml 파일 경로] --[결과 저장 경로] 
# example
# python main.py --yaml_path standard/middle.yaml --output_path .
```

## 검증 항목

1. 최종 산출물 분류 및 규모

    |순번|세부 산출물 명|목표수량|
    |------|---|---|
    |1|파라메트릭 모델|2개|
    |2|액터별 Shape 파라미터|22개|
    |3|액터별 템플릿|22개|
    |4|동작종류 메타 정보|1개|
    |5|카메라 파라미터 정보|4개|
    |6|2D 이미지|2,000,000|
    |7|2D 관절정보|2,000,000|
    |8|3D Shape 정보|500,000|
    |9|3D 관절 정보|500,000|
    |10|포인트 클라우드|25,000|
    |11|액터별 Shape 파라미터 - 액터별 템플릿|-|
    |12|2D 이미지 - 2D 관절정보|-|
    |13|3D Shape 정보 - 3D 관절정보|-|

2. 2D 조인트 좌표 정보 참값 정확도

    구축된 2D 조인트 좌표 정보에 대해 정확도 측정 
    OKS AP:0.5 기준 정확도 측정
    ![formular1]('./asset/formular_1.gif)
    
3. 3D 조인트 좌표 정보 참값 정확도

    구축된 3D 조인트 좌표 정보에 대해 정확도 측정
        - 각 조인트 항목의 평균 Accuracy
        - 정답의 판단은 아래 산출식을 이용
        ![formular2]('./asset/formular_2.gif)
        ![formular3]('./asset/formular_3.gif)
  