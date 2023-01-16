from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import render
from django.views import generic


def index(request: HttpRequest):
    return render(request, 'base.html')


class AccountView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'app_catalog/account.html'
    raise_exception = True
