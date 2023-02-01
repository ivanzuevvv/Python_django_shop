from django.urls import path
from .views import *

urlpatterns = [
    path('detail/', CartDetailView.as_view(), name='cart_detail'),
    path('add/<int:pk>/', cart_add, name='cart_add'),
    path('remove/<int:pk>/', cart_remove, name='cart_remove'),
    path('get_data/', get_cart_data, name='get_cart_data'),
    path('order/', OrderView.as_view(), name='create_order'),
    path('<int:pk>/', OrderDetail.as_view(), name='order_detail'),
    path('history/', HistoryOrders.as_view(), name='history'),
]
