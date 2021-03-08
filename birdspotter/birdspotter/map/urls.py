from django.urls import path

from . import views

urlpatterns = [
	path('<uuid>', views.index, name='index')
]