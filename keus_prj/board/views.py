from django.db.models import F
from django.core.exceptions import PermissionDenied
from .models import Board, Category
from django.views.generic import ListView
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BoardForm
from .models import predictData, predictData_storage
import pandas as pd
import os
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from django.http import JsonResponse
from datetime import datetime
import requests
from bs4 import BeautifulSoup


# Create your views here.
def index(request):
    boards = Board.objects.values('id', 'title', 'member__username', 'contents', 'created_at')
    return render(request, 'board/post.html', {'boards': boards})

def new_post(request):
    if request.method == 'POST':
        boards = BoardForm(request.POST)

        if boards.is_valid():
            print(boards.errors)
            boards.save()
            return redirect('board_list')
    else:
        boards = BoardForm()

    return render(request, 'board/new_post.html', {'boards': boards})

class PostList(ListView):
    model = Board
    template_name = 'board_list.html'
    context_object_name = 'board'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Board.objects.filter(category=None).count()
        return context

def post_detail(request, pk):
    board = get_object_or_404(Board, id=pk)
    posts = Post.objects.filter(board=board)
    return render(request, 'post_detail.html', {'board': board, 'posts': posts})

def delete_post(request, pk):
    board = get_object_or_404(Board, id=pk)

    if request.method == 'POST':
        board.delete()
        boards = Board.objects.order_by('id').values('id', 'title', 'member__username', 'created_at')

        with transaction.atomic():
            Board.objects.filter(id__gt=pk).update(id=F('id') - 1)

        data = {'message': '게시글이 삭제되었습니다.', 'boards': list(boards)}
        return JsonResponse(data)



    return render(request, 'board/delete_post.html', {'board': board})

def new_comment(request, pk):
    # 로그인 여부 확인
    if request.user.is_authenticated:
        # get_object_or_404 : 알맞지 않은 pk값이 넘어오면
        # 404 error를 발생시킨다.
        post = get_object_or_404(Post, pk=pk)

        if request.method == 'POST':
            # 사용자가 입력한 comment를 가지고
            # CommentForm의 인스턴스를 생성
            comment_form = CommentForm(request.POST)

            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        return redirect(post.get_absolute_url())
    else :
        raise PermissionDenied



# 지우면 안됨니다. 12월 1일 추가내용

def test(request):
    return render(request, 'board/test.html')

# 온도 데이터 LSTM 분석
def temp_lstm(request):
    print('데이터 분석 시작')
    # 데이터 경로 가져오기
    current_path = os.path.abspath(__file__)
    file_path_model = os.path.join(os.path.dirname(current_path), r'static\\bigdata\\온도 원본.xlsx')

    # 데이터 로드 및 전처리
    data = pd.read_excel(file_path_model)

    # '년월' 컬럼을 datetime 형식으로 변환
    data['년월'] = pd.to_datetime(data['년월'])

    # '연'과 '월' 컬럼 생성
    data['연'] = data['년월'].dt.year
    data['월'] = data['년월'].dt.month

    # '연'과 '월'을 기준으로 정렬
    data.sort_values(['연', '월'], inplace=True)

    # '연'과 '월'을 기준으로 index 재설정
    data.set_index(['연', '월'], inplace=True)

    # '시군구' 컬럼 제외한 데이터 선택, 예측하기 위한 데이터 선별
    features = ['평균기온(°C)', '평균최고기온(°C)', '평균최저기온(°C)']
    scaled_data = data[features]
    # 전처리 완료

    # 데이터 정규화
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(scaled_data)

    # 시퀀스 길이 정의
    seq_length = 12  # 예측에 사용할 과거 데이터의 개수

    # 시퀀스 데이터 생성
    X, y = create_sequences(scaled_data, seq_length)

    # LSTM 모델 정의
    model = Sequential()
    model.add(LSTM(50, activation='relu', input_shape=(seq_length, scaled_data.shape[1])))
    model.add(Dense(scaled_data.shape[1]))  # 출력 노드 수를 특성의 수와 같게 설정
    model.compile(optimizer='adam', loss='mse')  # 평균 제곱 오차 손실 함수 사용

    # LSTM 모델 훈련
    model.fit(X, y, epochs=50, batch_size=16)

    # 모델 평가
    loss = model.evaluate(X, y)
    print(f'Loss: {loss}')

    # 예측 데이터 생성
    predicted_data = []

    for i in range(len(scaled_data) - seq_length):
        seq = scaled_data[i:i+seq_length]
        seq = seq.reshape((1, seq_length, scaled_data.shape[1]))
        pred = model.predict(seq)
        predicted_data.append(pred)

    # 예측 데이터 역정규화
    predicted_data = scaler.inverse_transform(np.array(predicted_data).reshape(-1, scaled_data.shape[1]))

    # 소수 첫 번째 자리까지만 노출하고 두 번째 자리는 반올림
    predicted_data = np.round(predicted_data, decimals=1)

    features = ['예측 평균기온(°C)', '예측 평균최고기온(°C)', '예측 평균최저기온(°C)']
    # 예측 결과 출력
    predicted_df = pd.DataFrame(data=predicted_data,
                                columns=features,
                                 index=data.index[seq_length:])

    # 원본 데이터에서 예측 기간에 해당하는 부분 추출
    original_data = data.iloc[seq_length:]

    # 예측 데이터와 원본 데이터 결합
    result_df = pd.concat([original_data, predicted_df], axis=1)

    # 현재 날짜 및 시간을 가져옴
    current_datetime = datetime.now()

    # 생성 날짜 문자열 생성 (예: 20231130)
    creation_date_str = current_datetime.strftime('%Y%m%d')

    result_file_name = f'온도 예측데이터(전체)_{creation_date_str}.csv'
    save_path = os.path.join(os.path.dirname(current_path), r'static\\bigdata\\result\\',result_file_name)
    print('파일 저장 성공!')

    print('파일 불러오기!')
    # 예측 결과 및 실제 데이터 출력
    result_df.to_csv(save_path, index=False)
    print('파일 출력!',result_df)
    # csv 파일 저장 로직
    print('db에 경로저장 시작')
    db_save(save_path)
    print('db에 경로저장 종료')
    # result_df의 컬럼명 출력
    print(result_df.columns)

    # 데이터베이스에 저장
    for index, row in result_df.iterrows():
        # CSV 파일의 날짜 형식이 'YYYY-MM-DD'이므로 이를 datetime 객체로 변환
        predict_data = predictData(
            code=row['지점'],
            region=row['시군구'],
            date=row['년월'].date(),
            avg_temp=row['평균기온(°C)'],
            avg_max_temp=row['평균최고기온(°C)'],
            avg_min_temp=row['평균최저기온(°C)'],
            pre_avg_temp=row['예측 평균기온(°C)'],
            pre_avg_max_temp=row['예측 평균최고기온(°C)'],
            pre_avg_min_temp=row['예측 평균최저기온(°C)'],
        )
        predict_data.save()

    print("예측 결과와 실제 데이터를 엑셀 파일로 저장완료했습니다.")


    return JsonResponse({'status': 'success', 'message': '완료되었습니다.'})




# 시퀀스 생성 함수
def create_sequences(data, seq_length):
    sequences = []
    labels = []
    for i in range(len(data) - seq_length):
        seq = data[i:i+seq_length]
        label = data[i+seq_length]
        sequences.append(seq)
        labels.append(label)
    return np.array(sequences), np.array(labels)

# DB 파일 저장
def db_save(path):
    # 새로운 인스턴스 생성
    save_predictData_storage = predictData_storage()
    # 경로 저장, log 생성
    save_predictData_storage.csv_path = os.path.join(path)
    save_predictData_storage.created_at = datetime.now()
    # 저장
    save_predictData_storage.save()

def search_view(request):
    region = request.GET.get('region', None)
    print('성공',region)
    predicted_data = predictData.objects.filter(region=region).values()
    if predicted_data:
        return JsonResponse({'status': 'success', 'predicted_data': list(predicted_data)})
    else:
        return JsonResponse({'status': 'error', 'message': '지역 정보가 없습니다.'})

#날씨 크롤링
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