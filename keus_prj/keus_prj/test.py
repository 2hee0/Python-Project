import requests
import csv
import xml.etree.ElementTree as ET

url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst'
params ={'serviceKey' : 'mCikKhKL70povcSTSYtbdr4NnkcBwXiYRYMFPZNhN0Gp55WuGsTtvInPehZPAP3qxXJRi6G3FX9MJ2TPevKeHQ==', 'pageNo' : '1', 'numOfRows' : '1000', 'dataType' : 'XML', 'base_date' : '20231117', 'base_time' : '0600', 'nx' : '55', 'ny' : '127' }

response = requests.get(url, params=params)
# 응답 내용을 문자열로 디코딩
decoded_content = response.content.decode('utf-8')

# XML 형태로 파싱
xml_root = ET.fromstring(decoded_content)

# XML 트리를 문자열로 출력
pretty_xml = ET.tostring(xml_root, encoding='utf-8').decode('utf-8')
print(pretty_xml)

csv_file_path = 'output.csv'
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)

    # 헤더 작성
    header = ["baseDate", "baseTime", "category", "nx", "ny", "obsrValue"]
    csv_writer.writerow(header)

    # 각 item에서 필요한 정보 추출하여 CSV에 쓰기
    for item in xml_root.findall('.//item'):
        row = [item.findtext('baseDate'), item.findtext('baseTime'), item.findtext('category'),
               item.findtext('nx'), item.findtext('ny'), item.findtext('obsrValue')]
        csv_writer.writerow(row)

print(f'Data has been successfully saved to {csv_file_path}')