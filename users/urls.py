from django.urls import path
from . import views

urlpatterns = [
    path('', views.users), # 모든 회원 조회(GET), 회원 등록(POST)
    path('<str:user_id>', views.user),  # 회원로그인(POST), 회원정보조회(GET), 회원정보수정(PUT), 회원삭제(DELETE)
    path('register/<str:email>', views.email)   
]