from django.urls import path
from . import views

urlpatterns=[
    path('',views.index, name='board_list'),
    path('new_post/',views.new_post, name='post_write'),
    path('<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('post/delete/', views.delete_post_test, name='delete_post_test'),
    path('post/<int:pk>/add_comment/', views.add_comment, name='add_comment'),  # 댓글 추가
    path('test/',views.test),
    path('test/predict/',views.temp_lstm),
    path('search/', views.search_view),
    path('weather/', views.weather, name='weather'),
    path('electric/', views.electric, name='electric'),
    path('introduce/', views.introduce, name='introduce'),
    path('infographic/', views.infographic, name='infographic'),
]