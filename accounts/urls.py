from django.urls import path

from . import views

urlpatterns = [
    path('login1', views.login1, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
]
