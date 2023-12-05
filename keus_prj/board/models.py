from django.db import models
from django.conf import settings
from django.db.models.signals import post_migrate

# 카테고리 테이블
class Category(models.Model):
    objects = None
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200,unique=True, allow_unicode=True)
    #  allow_unicode=True : 한글을 포함한 모든 유니코드 문자를 지원

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/category/{self.slug}'

    class Meta:
        verbose_name_plural = 'Categories'

# 초기 카테고리 테이블 데이터 생성
# 초기 데이터 생성이나 특정 설정 변경과 같은 추가 작업에 활용
def create_initial_categories(sender, **kwargs):
    if Category.objects.count() == 0:
        Category.objects.create(name='Etc', slug='기타')                       # category_id = 1       일반
        Category.objects.create(name='Inquiry', slug='문의사항')                    # category_id = 2       문의
        Category.objects.create(name='Announcement', slug='공지사항')               # category_id = 3       공지사항

# post_migrate : 마이그레이션이 완료된 후에 실행
# post_migrate 신호에 create_initial_categories 함수 연결
post_migrate.connect(create_initial_categories)

class Board(models.Model):
    objects = None
    title = models.CharField(max_length=1200)
    contents = models.TextField(max_length=2000, default='값을 넣어주세요')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # null=True 제거
    file_upload = models.FileField(upload_to='board/images/%Y/%m/%d', blank=True)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL, blank=True)
    # 게시판 상태
    Board_Status = models.CharField(max_length=50, blank=True, null=True)


    def save(self, *args, **kwargs):
        # 기본 save() 메서드를 오버라이드하여 추가적인 동작을 수행
        # 카테고리가 할당된 경우우
        if self.category:
            # 보드의 Board_Status 필드에 카테고리의 이름을 할당
            self.Board_Status = self.category.slug
        # 기존의 save 메서드를 호출하여 보드 저장
        super(Board, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/board/{self.pk}'



class Comment(models.Model):
    objects = None
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    content = models.TextField(max_length=2000, default='값을 넣어주세요')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.member} :: {self.content}'

    def get_absolute_url(self):
        return f'{self.board.get_absolute_url()}#comment-{self.pk}'

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

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