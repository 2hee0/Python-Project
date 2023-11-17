from django.db import models

# Create your models here.

# main_member 테이블 작성
class Member(models.Model):
    member_id = models.CharField(max_length=200)    # 아이디
    member_pw = models.CharField(max_length=200)    # 비밀번호
    created_at = models.DateTimeField(auto_now_add=True)     # 가입일자
    updated_at = models.DateTimeField(auto_now=True)         # 수정일자


# board 테이블
class board(models.Model):
    title = models.CharField(max_length=1200)    # 리뷰 제목
    contents = models.TextField     # 글 작성란
    created_at = models.DateTimeField(auto_now_add=True)     # 작성일자
    updated_at = models.DateTimeField(auto_now=True)         # 수정일자