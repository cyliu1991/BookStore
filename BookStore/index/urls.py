from django.urls import path
from index import views

urlpatterns = [
    path('login/', views.login),
]