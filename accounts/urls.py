from django.urls import path
from . import views

urlpatterns = [
    path('', views.sign_up), # POST : 회원가입
    # path('user/', views.sign_in), # POST : 로그인
    path('email/', views.email), # GET:메일 중복확인 POST : 메일인증
    path('activate/', views.activate), # POST : 활성화
]