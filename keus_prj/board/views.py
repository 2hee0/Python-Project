from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import F
from .models import Board, Category, Comment, temp_rawdata, temp_predictData, temp_predictData_storage, Post
from django.views.generic import ListView
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BoardForm, CommentForm
import pandas as pd
import os
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from datetime import datetime
from django.contrib import messages
import json


# Create your views here.
def index(request):
    boards = Board.objects.values('id', 'title', 'member__username', 'contents', 'created_at', 'member', 'Board_Status')
    comments = Comment.objects.values('member', 'content', 'board', 'created_at', 'member__username')
    return render(request, 'board/post.html', {'boards': boards, 'comments': comments})

@login_required(login_url='member:login')
def new_post(request):
    # 231129 하승우 추가
    # 모든 카테고리 가져오기
    categories = Category.objects.all()
    # 현재 사용자가 스태프인지 확인
    is_staff = request.user.is_staff

    if request.method == 'POST':
        # 사용자가 입력한 데이터와 현재 로그인한 사용자 정보를 함께 저장
        boards = BoardForm(request.POST)
        if boards.is_valid():
            board = boards.save(commit=False)
            board.member = request.user  # 현재 로그인한 사용자 정보를 member 필드에 저장
            board.save()
            return redirect('board_list')
    else:
        boards = BoardForm()

    return render(request, 'board/new_post.html', {'boards': boards, 'categories': categories, 'is_staff': is_staff})

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

#수정
#수정
@login_required(login_url='member:login')
def delete_post(request, pk):
    board = get_object_or_404(Board, id=pk)
    # 출력
    print('board.member111 : ', board.member)
    print('request.user111 : ', request.user)

    # 작성자와 현재 로그인한 사용자가 같은지 확인
    if not (board.member == request.user or request.user.is_staff):             # request.user.is_staff 추가
        print('board.member : ', board.member)
        print('request.user : ', request.user)
        messages.error(request, '글 작성자 또는 스태프만 삭제할 수 있습니다.')
        return HttpResponseRedirect(reverse('board_list'))

    if request.method == 'POST':
        try:
            board.delete()
            with transaction.atomic():
                Board.objects.filter(id__gt=pk).update(id=F('id') - 1)

            # 게시글 삭제 후 board_list로 리다이렉션
            messages.success(request, '게시글이 성공적으로 삭제되었습니다.')
            return HttpResponseRedirect(reverse('board_list'))
            #return JsonResponse(jsonObject)

        except Exception as e:
            # 삭제 실패 메시지 출력
            print('exception : ', e)
            messages.error(request, f'게시글 삭제에 실패하였습니다. 원인: {str(e)}')

    return render(request, 'board/delete_post.html', {'board': board})


### 추가 시작
@login_required(login_url='member:login')
def delete_post_test(request):
    jsonObject = json.loads(request.body)
    pk = jsonObject.get('postId')
    board = get_object_or_404(Board, id=pk)

    print("board.member  ",board.member)
    print("request.user  ", request.user)

    # 작성자와 현재 로그인한 사용자가 같은지 확인
    if not (board.member == request.user or request.user.is_staff):  # request.user.is_staff 추가
        # messages.error(request, '글 작성자만 삭제할 수 있습니다.')
        # return HttpResponseRedirect(reverse('board_list'))
        return JsonResponse({'message': "글 작성자 또는 스태프만 삭제할 수 있습니다."})

    if request.method == 'POST':
        try:
            board.delete()
            with transaction.atomic():
                Board.objects.filter(id__gt=pk).update(id=F('id') - 1)

            # 게시글 삭제 후 board_list로 리다이렉션
            # messages.success(request, '게시글이 성공적으로 삭제되었습니다.')
            # return HttpResponseRedirect(reverse('board_list'))
            return JsonResponse({'message': "게시글이 성공적으로 삭제되었습니다."})

        except Exception as e:
            # 삭제 실패 메시지 출력
            print('exception : ', e)
            messages.error(request, f'게시글 삭제에 실패하였습니다. 원인: {str(e)}')

    return render(request, 'board/delete_post.html', {'board': board})

### 추가 끝

# def new_comment(request, pk):
#     # 로그인 여부 확인
#     if request.user.is_authenticated:
#         # get_object_or_404 : 알맞지 않은 pk값이 넘어오면
#         # 404 error를 발생시킨다.
#         board = get_object_or_404(Board, pk=pk)
#
#         if request.method == 'POST':
#             # 사용자가 입력한 comment를 가지고
#             # CommentForm의 인스턴스를 생성
#             comment_form = CommentForm(request.POST)
#
#             if comment_form.is_valid():
#                 comment = comment_form.save(commit=False)
#                 comment.board = board
#                 comment.author = request.user
#                 comment.save()
#                 return redirect(comment.get_absolute_url())
#         return redirect(board.get_absolute_url())
#     else :
#         raise PermissionDenied


#완성본
@staff_member_required
@login_required(login_url='member:login')
def add_comment(request, pk):
    board = get_object_or_404(Board, pk=pk)
    comments = Comment.objects.filter(board=board)
    comments_exist = comments.exists()  # 댓글 존재 여부 확인

    # 스태프만이 댓글을 추가할 수 있도록 확인
    if request.user.is_staff:
        if comments_exist:  # 댓글이 이미 존재하는 경우
            return JsonResponse({'comments_exist': True})
            # return HttpResponseForbidden("이미 댓글이 존재하여 추가할 수 없습니다.")

        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.board = board
                comment.member = request.user
                comment.save()
                return JsonResponse({'comments_exist': False})
                # return redirect('board_list')

        return render(request, 'board/post.html', {'form': comment_form, 'board': board})
    else:
        return HttpResponseForbidden("관리자만 댓글을 추가할 수 있습니다.")

# 지우면 안됨니다. 12월 1일 추가내용

def test(request):
    return render(request, 'board/test.html')

# 온도 데이터 LSTM 분석
def temp_lstm(request):
    print('데이터 분석 시작')
    # 데이터 경로 가져오기
    current_path = os.path.abspath(__file__)
    file_path_model = os.path.join(os.path.dirname(current_path), r'static\\bigdata\\온도 원본.xlsx')

    db_save(current_path)

    # 데이터 로드 및 전처리
    original_data = pd.read_excel(file_path_model)
    data = original_data.copy()

    for index, row in data.iterrows():
       temp_rawdata.objects.create(
            code=row['지점'],
            region=row['시군구'],
            date=row['년월'].date(),
            avg_temp=row['평균기온(°C)'],
            avg_max_temp=row['평균최고기온(°C)'],
            avg_min_temp=row['평균최저기온(°C)'],
            storage=some_existing_instance
        )



    # '년월' 컬럼을 datetime 형식으로 변환
    data['년월'] = pd.to_datetime(data['년월'])

    # '연'과 '월' 컬럼 생성
    data['연'] = data['년월'].dt.year
    data['월'] = data['년월'].dt.month

    # '시군구', '연'과 '월'을 기준으로 정렬
    data.sort_values(['시군구', '연', '월'], inplace=True)

    # '시군구', '연'과 '월'을 기준으로 index 재설정
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
    original_data = original_data.iloc[seq_length:]

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
        predict_data = temp_predictData(
            code=row['지점'],
            region=row['시군구'],
            date=row['년월'].date(),
            avg_temp=row['평균기온(°C)'],
            avg_max_temp=row['평균최고기온(°C)'],
            avg_min_temp=row['평균최저기온(°C)'],
            pre_avg_temp=row['예측 평균기온(°C)'],
            pre_avg_max_temp=row['예측 평균최고기온(°C)'],
            pre_avg_min_temp=row['예측 평균최저기온(°C)'],
            storage=some_existing_instance,
            rawdata=some_existing_instance,
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

# DB에 파일 저장
def db_save(path):
    # 새로운 인스턴스 생성
    save_predictData_storage = temp_predictData_storage()
    # 경로 저장, log 생성
    save_predictData_storage.csv_path = os.path.join(path)
    save_predictData_storage.created_at = datetime.now()
    # 저장
    save_predictData_storage.save()

def search_view(request):
    region = request.GET.get('region', None)
    print('성공',region)
    raw_data = temp_rawdata.objects.filter(region=region).values()
    if raw_data:
        return JsonResponse({'status': 'success', 'predicted_data': list(raw_data)})
    else:
        return JsonResponse({'status': 'error', 'message': '지역 정보가 없습니다.'})

def weather(request):
    # 데이터 검색
    region = request.GET.get('region')
    year = request.GET.get('year')
    # search_data = temp_rawdata.objects.filter(region=region, date__year=year)
    search_data = temp_rawdata.objects.filter(region=region, date__year=year).values('id').annotate(max_id=Max('id'))
    # 중복 제거하고 최신 데이터만 가져옴
    search_data = temp_rawdata.objects.filter(id__in=search_data.values('max_id'))

    return render(request, 'board/weather.html', {'search_data':search_data})


def electric(request):
    return render(request, 'board/electric.html')


def introduce(request):
    return render(request, 'board/introduce.html')


def infographic(request):
    return render(request, 'board/infographic.html')