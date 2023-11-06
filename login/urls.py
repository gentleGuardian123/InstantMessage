# swt&&zwx
# time: 2023/6/5 10:46

from .views import signup, login, forget, send_vericode
from django.urls import path

urlpatterns = [
    path('login/', login, name='login'),
    path('signup/', signup, name='signup'),
    path('forget/', forget, name='forget'),
    path('send_vericode', send_vericode, name='send_vericode')
]
