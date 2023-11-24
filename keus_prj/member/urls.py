from django.urls import path
from . import views
from .views import join

urlpatterns=[
    # localhost:8000/blog 매핑
    path('join/',views.join, name='join'),
    path('login/', views.login, name='login'),
    path('header/', views.header, name='header'),
    path('find/', views.find, name='find'),
    path('check_username/', views.check_username, name='check_username'),
]