from django.shortcuts import render, redirect, get_object_or_404
from .forms import BoardForm
from member.models import Board

# 날씨 관련 api필요 임포트
import requests
from datetime import datetime
# 날씨 api



# Create your views here.
def index(request):
    boards = Board.objects.all()
    return render(request, 'post.html', {'boards': boards})


def new_post(request):
    # Board 모델을 사용하여 데이터를 불러올 수 있음
    if request.method == 'POST':
        boards = BoardForm(request.POST)
        if boards.is_valid():
            boards.save()  # Board 모델에 데이터 저장
            return redirect('/board')  # 게시글 목록으로 리다이렉트
    else:
        boards = BoardForm()

    return render(request, 'new_post.html', {'boards': boards})

def post_detail(request, pk):
    board = get_object_or_404(Board, id=pk)
    return render(request, 'post_detail.html', {'board': board})