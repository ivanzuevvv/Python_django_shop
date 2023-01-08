from django.contrib import admin
from django.contrib.auth.models import AbstractUser, Group
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, RegexValidator
from django.db import models
from django.utils.safestring import mark_safe

from .managers import UserManager


class User(AbstractUser):
    image_validator = FileExtensionValidator(
        allowed_extensions=['png', 'jpg', 'gif'],
        message='Расширение не поддерживается. Разрешенные расширения .jpg .gif .png')

    def validate_size(fieldfile_obj):
        filesize = fieldfile_obj.file.size
        megabyte_limit = 2.0
        if filesize > megabyte_limit * 1024 * 1024:
            raise ValidationError("Максимальный размер файла %sMB" % str(megabyte_limit), code='invalid')

    phoneNumberValid = RegexValidator(regex=r"^\d{10}$")

    phone = models.CharField(unique=True, validators=[phoneNumberValid], max_length=10, verbose_name="Телефон")
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    username = models.CharField(blank=True, max_length=30, default='', verbose_name="Никнейм")
    second_name = models.CharField(max_length=30, verbose_name='Отчество', blank=True, default='')
    avatar = models.ImageField(upload_to='avatars/', blank=True, verbose_name='Ссылка на изображение',
                               validators=[validate_size, image_validator])
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.second_name}' if self.second_name \
            else f'{self.last_name} {self.first_name}'

    @admin.display(description='Полное имя')
    def get_full_name(self):
        full_name = "%s %s %s" % (self.last_name, self.first_name, self.second_name)
        return full_name.strip()

    @admin.display(description='Изображение')
    def get_image_avatar(self):
        if self.avatar:
            return mark_safe(f'<img src={self.avatar.url} height="50"')
        else:
            return 'Нет изображения'

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class ProxyGroups(Group):
    class Meta:
        proxy = True
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
