from django.urls import path
from .models import UserInfo
from users import views

app_name = 'users'

urlpatterns = [
    path('register/', views.Register.as_view(), name='register'),
    path('login/', views.Login.as_view(), name='login'),
    path('loginout/', views.LoginOut.as_view(), name='loginout'),
    path('get_auth_img/', views.GetAuthImg.as_view(), name="get_auth_img"),
]
