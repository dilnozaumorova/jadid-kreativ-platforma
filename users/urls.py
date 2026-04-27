from django.urls import path

from users.views import UserRegisterView,UserLoginView,UserLogoutView



urlpatterns=[
    path('register',UserRegisterView,name='register'),
    path('login',UserLoginView,name='login'),
    path('logout',UserLogoutView,name='logout'),
]