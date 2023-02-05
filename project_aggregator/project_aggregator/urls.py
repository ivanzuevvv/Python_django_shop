"""project_aggregator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from . import settings

urlpatterns = [
    path('', include('app_products.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('app_users.urls')),
    path('buy/', include('app_movement_goods.urls')),
    path('payment/', include('app_payments.urls')),
    path('debug/', include('debug_toolbar.urls')),
    path('catalog/', include('app_filter_catalog.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
