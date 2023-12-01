from django.urls import path
from . import views
<<<<<<< HEAD

urlpatterns=[
    path('',views.index),
    path('new_post/',views.new_post),
    path('<int:pk>/', views.post_detail),
=======
from .views import post_detail, delete_post

urlpatterns=[
    path('',views.index, name='board_list'),
    path('new_post/',views.new_post, name='post_write'),
    path('<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/delete/', delete_post, name='delete_post'),
    path('<int:pk>/new_comment/',views.new_comment),
>>>>>>> 5300eb95c0d7ea7cc17b9ef5baf1824939fa8c83
]