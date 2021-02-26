from django.urls import path, include

from . import views

urlpatterns = [
    path('profile/', views.account_view),
    path('login/', views.login_view),
    path('logout/', views.logout_view),
    path('register/', views.register_view),
    path('request_group/', views.request_privileged_view),
    path('group_requests/', views.group_request_view),
    path('group_requests/<uuid:request_id>/<str:action>', views.process_request_action),
    path('', include('django.contrib.auth.urls'))]
    