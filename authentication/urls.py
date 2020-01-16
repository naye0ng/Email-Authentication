from django.urls import path
from . import views

urlpatterns = [
    path('authentiaction/', views.authentiaction),
]