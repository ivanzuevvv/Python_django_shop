# from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

from app_users.models import User

# User = get_user_model()


class RegUserForm(UserCreationForm):
    password1 = forms.CharField(
        max_length=150, required=True, widget=forms.PasswordInput(
            attrs={'class': 'form-input', 'data-validate': 'requirePassword',
                   'placeholder': 'Введите пароль', 'autocomplete': 'new-password',
                   'maxlength': '150'}))
    password2 = forms.CharField(
        max_length=150, required=True, widget=forms.PasswordInput(
            attrs={'class': 'form-input', 'data-validate': 'requireRepeatPassword',
                   'placeholder': 'Введите пароль повторно', 'autocomplete': 'new-password',
                   'maxlength': '150'}))
    full_name = forms.CharField(
        max_length=254, required=True, widget=forms.TextInput(
            attrs={'class': 'form-input', 'data-validate': 'require', 'placeholder': 'Введите ФИО',
                   'maxlength': '254'}))
    email = forms.EmailField(
        max_length=254, label='e-mail', required=True, widget=forms.TextInput(
            attrs={'class': 'form-input', 'data-validate': 'requireMail', 'maxlength': '254'}))
    phone = forms.CharField(
        required=True, widget=forms.TextInput(attrs={'class': 'form-input', 'data-validate': 'requirePhone'}))
    avatar = forms.ImageField(required=False, widget=forms.ClearableFileInput(
        attrs={'class': 'Profile-file form-input', 'type': "file",
               'accept': ".jpg,.gif,.png", 'data-validate': "onlyImgAvatar"}))

    class Meta:
        model = User
        fields = ('password1', 'password2', 'email', 'phone')
