from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import RegUserForm
from .models import User


class RegistrationView(CreateView):
    model = User
    form_class = RegUserForm
    template_name = 'app_users/registration.html'
    success_url = reverse_lazy('main')

    def post(self, request, *args, **kwargs):
        form = RegUserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            my_group, result = Group.objects.get_or_create(name="Покупатели")
            my_group.user_set.add(user)
            login(request, user)
            return HttpResponseRedirect(self.success_url)
        return self.form_invalid(form)
