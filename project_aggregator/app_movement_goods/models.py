from decimal import Decimal

from django.conf import settings
from django.db import models

from app_catalog.models import Product


class UserCart(models.Model):
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='cart', verbose_name='Чья корзина', blank=True, null=True)
    session = models.CharField(
        verbose_name='Сессия', blank=True, null=True, max_length=40)
    cart = models.ManyToManyField(
        Product, through='InsideCart', verbose_name='Содержание корзины',
        related_name="carts", blank=True)

    def __str__(self):
        return 'Корзина ' + str(self.owner.email) if self.owner else 'Anonymous'

    def __len__(self):
        return sum(item.quantity for item in self.contents.only('quantity').all())

    def add(self, product, quantity=1, update_quantity=False):
        cart = self.contents.get_or_create(user_cart=self, goods=product)[0]
        if update_quantity:
            cart.quantity = quantity
        else:
            cart.quantity += quantity
        # cart.cost = str(product.price)
        cart.save()

    def remove(self, product):
        self.cart.remove(product)

    @property
    def get_total_price(self):
        return sum(
            Decimal(item.cost) * item.quantity for item in self.contents.only('quantity', 'cost').all())

    def clear(self):
        self.delete()

    class Meta:
        verbose_name = "Корзина пользователя"
        verbose_name_plural = "Корзины пользователей"


class InsideCart(models.Model):
    user_cart = models.ForeignKey(UserCart, on_delete=models.CASCADE, related_name='contents')
    goods = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товары')
    quantity = models.PositiveSmallIntegerField(verbose_name='Количество', default=0)
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость', null=True)

    def __str__(self):
        return f'{self.goods}={self.quantity} шт.'

    def save(self, *args, **kwargs):
        if not self.cost:
            self.cost = str(self.goods.price)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


"""
from app_movement_goods.models import UserCart
from app_catalog.models import Product
from app_users.models import User
user = User.objects.get(pk=9)
prod1 = Product.objects.get(pk=10)
prod2 = Product.objects.get(pk=15)
prod3 = Product.objects.get(pk=23)
cart = UserCart.objects.get_or_create(owner=user)[0]
"""
