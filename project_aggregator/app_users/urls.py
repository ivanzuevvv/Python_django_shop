from django.urls import path, include

from .views import *

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('reg/', RegistrationView.as_view(), name='registration'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('order/', OrderRegView.as_view(), name='registration_order'),
]
