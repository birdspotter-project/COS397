from django.urls import path

from . import views

urlpatterns = [
    path('profile/', views.account_view),
    path('login/', views.login_view),
    path('logout/', views.logout_view)]
