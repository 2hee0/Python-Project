from django.db import models
from django.conf import settings
from enum import Enum

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
    # category에 외래키 걸기
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/board/{self.pk}'

class Comment(models.Model):
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    content = models.TextField(max_length=2000, default='값을 넣어주세요')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author} :: {self.content}'

    def get_absolute_url(self):
        return f'{self.post.get_absolute_url()}#comment-{self.pk}'

class predictData_storage(models.Model):
    # 파일 저장 경로
    csv_path = models.CharField(max_length=255)
    # log data
    created_at = models.DateTimeField(auto_now_add=True)

class predictData(models.Model):
    # predictData_storage  fk설정
    storage_id = models.ForeignKey(predictData_storage, null=True, on_delete=models.SET_NULL)
    # 지점
    code = models.IntegerField()
    # 시군구
    region = models.CharField(max_length=255)
    # 년월
    date = models.DateField()
    # 평균 온도
    avg_temp = models.FloatField()
    # 평균 최고 온도
    avg_max_temp = models.FloatField()
    # 평균 최소 온도
    avg_min_temp = models.FloatField()
    # 예측 평균 온도
    pre_avg_temp = models.FloatField()
    # 예측 평균 최고 온도
    pre_avg_max_temp = models.FloatField()
    # 예측 평균 최소 온도
    pre_avg_min_temp = models.FloatField()

    def __str__(self):
        return f"{self.date} - {self.region} - {self.avg_temp}"

class predict_future_Data(models.Model):
    # 지점
    code = models.IntegerField()
    # 시군구
    region = models.CharField(max_length=255)
    # 년월
    date = models.DateField()
    # 예측 평균 온도
    pre_avg_temp = models.FloatField()
    # 예측 평균 최고 온도
    pre_avg_max_temp = models.FloatField()
    # 예측 평균 최소 온도
    pre_avg_min_temp = models.FloatField()