from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView

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


class ProfileView(LoginRequiredMixin, UpdateView):
    raise_exception = True
    form_class = RegUserForm
    model = User
    template_name = 'app_users/profile.html'

    def get_success_url(self):
        return reverse('profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.info(self.request, "Профиль успешно сохранен")
        return super(ProfileView, self).form_valid(form)


class OrderRegView(RegistrationView):
    success_url = reverse_lazy('create_order')

