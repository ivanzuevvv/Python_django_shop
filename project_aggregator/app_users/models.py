from django.contrib import admin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, Group, PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    image_validator = FileExtensionValidator(
        allowed_extensions=['png', 'jpg', 'gif'],
        message='Расширение не поддерживается. Разрешенные расширения .jpg .gif .png')

    def validate_size(self):
        filesize = self.file.size
        print(self.file.size)
        megabyte_limit = 2.0
        if filesize > megabyte_limit * 1024 * 1024:
            raise ValidationError("Максимальный размер файла %sMB" % str(megabyte_limit), code='invalid')

    phoneNumberValid = RegexValidator(regex=r"^\d{10}$")

    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    phone = models.CharField(unique=True, validators=[phoneNumberValid], max_length=10, verbose_name="Телефон")
    full_name = models.CharField(max_length=254, verbose_name='Полное имя', default='')
    avatar = models.ImageField(upload_to='avatars/', blank=True, verbose_name='Ссылка на изображение',
                               validators=[validate_size, image_validator])
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='Дата регистрации')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    is_staff = models.BooleanField(default=False, verbose_name='Сотрудник')
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.full_name

    @property
    def welcome_name(self):
        return ' '.join(self.full_name.split()[1:])

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
