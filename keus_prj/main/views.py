from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from board.models import Board
# Create your views here.
def index(request):
    boards = Board.objects.values('id', 'title', 'member__username')
    tags = get_weather_info(request)
    return render(request, 'main/index.html',{'tags': tags, 'boards': boards})

# 날씨 관련 크롤링
def get_weather_info(request):
    url = "https://weather.com/ko-KR/weather/today/l/86a344a14f9715ce3ebdb0e167971a17de07d95eebf0dc29e450f8bd89c73678"
    res = requests.get(url)
    res.raise_for_status()  # 정상 200
    soup = BeautifulSoup(res.text, "lxml")

    tags = soup.select(".CurrentConditions--columns--30npQ")

    weather_data = []
    for tag in tags:
        temp_high_low = tag.find(class_='CurrentConditions--tempHiLoValue--3T1DG')
        temp_high = temp_high_low.find_all('span', {'data-testid': 'TemperatureValue'})[0].text
        temp_low = temp_high_low.find_all('span', {'data-testid': 'TemperatureValue'})[1].text

        weather = {
            'temperature': tag.find(class_='CurrentConditions--tempValue--MHmYY').text,
            'phrase': tag.find(class_='CurrentConditions--phraseValue--mZC_p').text,
            'temp_high': temp_high,
            'temp_low': temp_low,
        }
        weather_data.append(weather)
    print('weather_data 불러오기' )
    return weather_data