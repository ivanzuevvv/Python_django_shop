from django.conf import settings
from django.db import models
from django.utils.timezone import now

from app_catalog.models import Product


class CommentProduct(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='comments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='товар', related_name='comments')
    content = models.TextField(verbose_name='отзыв', max_length=300)
    pub_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    edit_at = models.DateTimeField(auto_now=True, verbose_name='дата редактирования')
    hide_on = models.BooleanField(verbose_name='Скрыт', default=False)

    def __str__(self):
        return f'Отзыв к {self.product}'

    def save(self, *args, **kwargs):
        if self.hide_on:
            self.content = f'{self.content}\n\n Скрыто модератором {now}'
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
