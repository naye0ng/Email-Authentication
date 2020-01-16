from django.urls import path
from . import views

urlpatterns = [
    path('', views.login),
    path('validate/', views.validate),
    path('refresh/', views.refresh),
]