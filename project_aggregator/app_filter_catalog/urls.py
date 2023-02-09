from django.urls import path

from .views import *

urlpatterns = [
    path('', ProductByCategoryView.as_view(), name='catalog'),
    path('<str:slug>/', ProductByCategoryView.as_view(), name='product_by_category'),
]
