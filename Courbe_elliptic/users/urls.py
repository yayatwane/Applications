from django.urls import path
from users import views


urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('upload', views.upload),
    path('verifier', views.verification)
]
