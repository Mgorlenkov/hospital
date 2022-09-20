from django.contrib.auth import views
from django.urls import path

from .views import *

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('blank/<str:id>', blank),
    path('download/<str:nIb>', download),
    path('glikProfile/<str:nIb>', glikProfile),
    path('pin-list/<str:nIb>', pinList),
    path('water/<str:nIb>', water),
    path("edit/<str:id>", editPacient, name="editPacient"),
    path('', index, name='home')
]