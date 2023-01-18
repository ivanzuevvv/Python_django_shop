from django.urls import path

from .views import *

urlpatterns = [
    path('', ShopView.as_view(), name='main'),
    path('account/', AccountView.as_view(), name='account'),
]
