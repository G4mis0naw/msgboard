from django.urls import path

from . import views

urlpatterns = [
    path('', views.message_board),
    path('submit', views.message_submit),
]