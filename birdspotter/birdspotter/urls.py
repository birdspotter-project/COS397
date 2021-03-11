"""birdspotter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
import private_storage.urls

from birdspotter.dataio.views import share_dataset

urlpatterns = [
    path('', views.index, name='index'),
    path('data/', include('birdspotter.dataviz.urls')),
    path('map/', include('birdspotter.map.urls')),
    path('import/', include('birdspotter.dataio.urls')),
    path('accounts/', include('birdspotter.accounts.urls')),
    path('queue/', include('birdspotter.analysis.urls')),
    path('edit/<uuid>', views.edit_dataset),
    path('admin/', admin.site.urls),
    path('health/', include('health_check.urls')),
    path('private-media/', include(private_storage.urls)),
    path('auth/', views.auth, name='auth'),
    path('share/<uuid:dataset_id>/', share_dataset)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # only works in dev mode
