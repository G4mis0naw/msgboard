from django.urls import path

from . import views, forms

urlpatterns = [
    path('', views.index, name="index"),
    #path('', views.login, name="login"),
    path('', forms.msgForm, name="msgForm"),
]