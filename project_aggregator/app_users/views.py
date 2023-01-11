from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import RegUserForm
from .models import User


class RegistrationView(CreateView):
    model = User
    form_class = RegUserForm
    template_name = 'app_users/registration.html'
    success_url = reverse_lazy('login')
