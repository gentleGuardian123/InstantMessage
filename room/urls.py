# swt&&zwx
# time: 2023/6/7 16:47

from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='chat-view'),
    path('<str:room_name>/<str:user_name>/', views.room_view, name='chat-room'),
    path('logout/', views.logout, name='logout'),
]
