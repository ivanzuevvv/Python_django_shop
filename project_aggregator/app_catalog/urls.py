from django.urls import path

from .views import *

urlpatterns = [
    path('', ShopView.as_view(), name='main'),
    path('good/<str:slug>/', ProductDetalView.as_view(), name='product_detail')
]
