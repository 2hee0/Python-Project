from django.urls import path
from . import views

urlpatterns=[
    # localhost:8000/blog 매핑
    path('',views.index),

]