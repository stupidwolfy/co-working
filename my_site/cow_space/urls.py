from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.cow_login, name='login'),
    path('logout/', views.cow_logout, name='logout'),
    path('topup/', views.topup, name='topup'),
]
