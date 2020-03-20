from django.conf.urls import url
from django.urls import path, include

from . import views

app_name = "message"

urlpatterns = [
    path('', views.message_board),
    url(r'login/', views.login_box, name='login'),
    url(r'signup/', views.signup_box, name='signup'),
    url(r'index/', views.message_board, name='index'),
    url(r'submit', views.message_submit, name='submit'),
    url(r'register', views.register, name='register'),
    url(r'login', views.login, name='loginsubmit'),
]