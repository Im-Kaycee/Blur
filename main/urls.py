from django.urls import path
from . import views
from .views import user_register

urlpatterns = [
    path('login/', views.user_login, name='user_login'),
    path('register/', user_register.as_view(), name='register'),
    path('logout/', views.user_logout, name='user_logout'),
]
