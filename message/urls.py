from json import tool
from django.conf.urls import url
from . import views

app_name = "message"

urlpatterns = [

    url(r'^$', views.home),
    url(r'home', views.home, name='home'),
    url(r'login', views.login, name='login'),
    url(r'register', views.register, name='register'),
    url(r'logout', views.logout, name='logout'),
    url(r'post', views.message, name='post'),
    url(r'delete/(?P<id>.*)/$', views.delete, name='delete'),
]