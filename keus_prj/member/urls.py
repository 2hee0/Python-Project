from django.urls import path
from . import views
from .views import join

app_name = 'member'  # 네임스페이스 추가

urlpatterns=[
    path('join/',views.join, name='join'),
    path('login/', views.login, name='login'),
    path('find/', views.find, name='find'),
    path('check_username/', views.check_username, name='check_username'),
    path('logout/', views.logout, name='logout'),
    path('mypage/', views.mypage, name='mypage'),
    path('check_email/', views.check_email, name='check_email'),
    path('check_tell/', views.check_tell, name='check_tell'),
]