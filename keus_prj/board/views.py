from django.shortcuts import render, redirect, get_object_or_404
from .forms import BoardForm
from .models import Board, Category
from django.views.generic import ListView
from django.http import JsonResponse
from django.db.models import F
from django.db import transaction


# 날씨 관련 api필요 임포트
import requests
from datetime import datetime

# Create your views here.
def index(request):
    boards = Board.objects.values('id', 'title', 'member__username', 'contents', 'created_at')
    return render(request, 'board/post.html', {'boards': boards})

from django.shortcuts import render, redirect, get_object_or_404
from .forms import BoardForm
from .models import Board, Category
from django.views.generic import ListView
from django.http import JsonResponse
from django.db.models import F
from django.db import transaction

# 날씨 관련 api필요 임포트
import requests
from datetime import datetime

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




