import requests
from openpyxl import Workbook

# API 키와 엔드포인트 정의
api_key = 'k0rTUY6Dq8LEYa03REnA10T3A3Q824pq1mnw933J'
endpoint = 'https://bigdata.kepco.co.kr/openapi/v1/powerUsage/contractType.do'

# 엑셀 파일 생성
workbook = Workbook()
sheet = workbook.active

# 열 제목 정의
headers = ['year', 'month', 'metro', 'city', 'cntr', 'custCnt', 'powerUsage', 'bill', 'unitCost']
# 시트에 제목 추가
sheet.append(headers)

# 시작 연도와 끝 연도 설정
start_year = 2019
end_year = 2022

start_month = 1
end_month = 12

# 요청 파라미터 설정 및 데이터 수집
for year in range(start_year, end_year + 1):
    for month in range(start_month, end_month + 1):
        params = {
            'year': year,
            'month': month,
            'metroCd': 11,
            'cntrCd': 600,
            'apiKey': api_key,
            'returnType': 'json'
        }

        # API 불러오기
        response = requests.get(endpoint, params=params)

        # 응답 확인
        if response.status_code == 200:
            # data 키의 값 가져오기
            data_list = response.json().get('data', [])

            # 데이터 리스트에 있는 각 데이터를 시트에 추가
            for data in data_list:
                sheet.append([data.get(key, '') for key in headers])

# 파일 저장
workbook.save('test2.xlsx')