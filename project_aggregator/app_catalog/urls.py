from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='main'),
    path('account/', AccountView.as_view(), name='account'),
]
