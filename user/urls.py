from django.urls import path

from . import views

urlpatterns = [
     path('', views.signup_box),
     path('register', views.register),
]