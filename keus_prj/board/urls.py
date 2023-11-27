from django.urls import path
from . import views

urlpatterns=[
    path('',views.index),
    path('new_post/',views.new_post),
    path('<int:pk>/', views.post_detail),
]