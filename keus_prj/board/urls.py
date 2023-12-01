from django.urls import path
from . import views

urlpatterns=[
    path('',views.index, name='board_list'),
    path('new_post/',views.new_post, name='post_write'),
    path('<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('<int:pk>/new_comment/',views.new_comment),
    path('test/',views.test),
    path('test/predict/',views.temp_lstm),
    path('search/', views.search_view),
]