from django.db import models
from django.conf import settings
# 이넘 사용
from enum import Enum
# User테이블에 컬럼 추가하기위한 import
from django.contrib.auth.models import AbstractUser, User
# Create your models here.

# enum 설정
class MemberStatus(Enum):
    # 가입, 활동 상태
    ACTIVE = 'active'
    # 탈퇴 상태
    INACTIVE = 'inactive'

class BoardStatus(Enum):
    # 일반글
    NORMAL = 'normal'
    # 문의글
    INQUIRY = 'inquiry'
    # 공지글
    ANNOUNCEMENT = 'announcement'

# 카테고리 테이블
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200,
                            unique=True, allow_unicode=True)
    #  allow_unicode=True : 한글을 포함한 모든 유니코드 문자를 지원

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/category/{self.slug}'

    class Meta:
        verbose_name_plural = 'Categories'

# main_member 테이블 작성
class Member(AbstractUser):
    # 주소
    Address = models.CharField(max_length=1000)
    # 전화번호
    Tell = models.CharField(max_length=200)         
    # 멤버 관련 이넘
    Member_Status = models.CharField(
        max_length=20,
        choices=[(status.value, status.name) for status in MemberStatus],
        default=MemberStatus.ACTIVE.value
    )
    # 수정일자
    updated_at = models.DateTimeField(auto_now=True)         


# board 테이블
class Board(models.Model):
    # 리뷰 제목
    title = models.CharField(max_length=1200)
    # 글 작성란
    contents = models.TextField(max_length=2000, default='값을 넣어주세요')
    # 작성일자
    created_at = models.DateTimeField(auto_now_add=True)
    # 수정일자
    updated_at = models.DateTimeField(auto_now=True)                            
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    # 보드 관련 이넘
    Board_Status = models.CharField(
        max_length=20,
        choices=[(status.value, status.name) for status in BoardStatus],
        default=BoardStatus.NORMAL.value
    )
    # 파일 업로드
    file_upload = models.FileField(upload_to='board/images/%Y/%m/%d', blank=True)
    # 댓글
    Review = models.TextField(max_length=2000, default='값을 넣어주세요')
    # category에 외래키 걸기
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL, blank=True)
    
# class Board_Review(models.Model):
#     # Member  fk설정
#     member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     # Board fk설정
#     board = models.ForeignKey(Board, on_delete=models.CASCADE)
#     # 리뷰 작성란
#     Re_Contents = models.TextField(max_length=2000, default='값을 넣어주세요')
#     # 작성일자
#     created_at = models.DateTimeField(auto_now_add=True)