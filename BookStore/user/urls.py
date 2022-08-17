from django.urls import path
from user import views
urlpatterns = [
    path('login/', views.login_view),
    path('logout/', views.logout_view),
    path('reg/', views.reg_view)
]