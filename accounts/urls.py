from django.urls import path
from . import views


urlpatterns = [
    path('register', views.RegisterAPI.as_view()),
    path('login', views.LoginAPI.as_view()),
    path('refresh', views.RefreshTokenAPI.as_view()),
    path('profile/me', views.MyProfile.as_view()),
]

    