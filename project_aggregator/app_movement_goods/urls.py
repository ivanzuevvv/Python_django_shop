from django.urls import path
from .views import *

urlpatterns = [
    path('detail/', CartDetailView.as_view(), name='cart_detail'),
    path('add/<int:pk>/', cart_add, name='cart_add'),
    path('remove/<int:pk>/', cart_remove, name='cart_remove'),
    path('get_data/', get_cart_data, name='get_cart_data'),
]