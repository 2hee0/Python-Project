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

# main_member 테이블 작성
class Member(AbstractUser):
    # 주소, 현재 빼둠
    # Address = models.CharField(max_length=1000)
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