from django.contrib import admin
from .models import Board, Comment, Category


# Board 모델을 위한 Admin 설정
@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    # BoardAdmin 클래스에 CommentInline 클래스 추가
    class CommentInline(admin.StackedInline):
        model = Comment
        extra = 0  # 추가적으로 입력할 수 있는 Comment 폼의 개수

    # BoardAdmin에 CommentInline 추가
    inlines = [CommentInline]

    # Admin 패널에서 보여질 목록 설정
    list_display = ('id', 'title', 'contents', 'member', 'created_at', 'category')
    list_display_links = ('title',)  # title을 클릭하면 해당 게시글의 변경 페이지로 이동
    search_fields = ('title', 'category', 'member')  # 제목, 카테고리, 작성자로 검색 가능
    list_filter = ('created_at',)  # 작성일을 기준으로 필터링 가능

    # 게시글 제목 반환하는 함수
    def board(self, obj):
        return obj.title


# Comment 모델을 위한 Admin 설정
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    # Admin 패널에서 보여질 목록 설정
    list_display = ('id', 'content', 'board', 'member', 'created_at')
    list_display_links = ('content',)  # 댓글 내용을 클릭하면 해당 댓글의 변경 페이지로 이동
    search_fields = ('member__username', 'board__title', 'content')  # 작성자, 게시글 제목, 내용으로 검색 가능
    list_filter = ('created_at',)  # 작성일을 기준으로 필터링 가능

    # 댓글이 속한 게시글의 제목 반환하는 함수
    def board(self, obj):
        return obj.board.title

    # board 필드를 기준으로 정렬
    board.admin_order_field = 'board__title'
