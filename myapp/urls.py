from django.contrib import admin
from django.urls import path, include
from . import views
from .middlewares.auth import auth_middleware

urlpatterns = [
    path('', views.Index.as_view(), name='Home'),
    path('signup/', views.Signup.as_view(), name='Signup'),
    path('login/', views.Login.as_view(), name='Login'),
    path('logout/', views.logout, name='Logout'),
    path('bus_result/', views.Search_bus.as_view(), name='SearchBus'),
    path('see-booking/', auth_middleware(views.SeeBooking.as_view()), name='SeeBooking'),
]
