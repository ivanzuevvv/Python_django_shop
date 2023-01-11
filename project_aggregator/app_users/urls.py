from django.urls import path, include

from .views import RegistrationView

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('reg/', RegistrationView.as_view(), name='registration'),
]
