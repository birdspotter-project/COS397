from django.urls import path, include

from . import views

urlpatterns = [
    path('profile/', views.account_view),
    path('login/', views.login_view),
    path('logout/', views.logout_view),
    path('register/', views.register_view),
    path('request_group/', views.request_privleged_view),
    path('', include('django.contrib.auth.urls'))]
    