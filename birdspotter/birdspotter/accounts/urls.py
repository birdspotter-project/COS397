from django.urls import path
import django.contrib.auth.urls

from . import views

urlpatterns = [
	path('login/', views.login, name='login')
]