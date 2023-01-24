from decimal import Decimal

from django.conf import settings
from django.db import models

from app_catalog.models import Product


class UserCart(models.Model):
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='cart', verbose_name='Чья корзина', blank=True)
    session = models.TextField(verbose_name='Сессия', default='')
    cart = models.ManyToManyField(
        Product, through='InsideCart', verbose_name='Содержание корзины',
        related_name="carts", blank=True, null=True)

    def __str__(self):
        return 'Корзина ' + str(self.owner) if self.owner else 'Anonymous'

    def add(self, product, quantity=1, update_quantity=False):
        cart = InsideCart.objects.get_or_create(
            user_cart=self, goods=product)[0]
        if update_quantity:
            cart.quantity = quantity
        else:
            cart.quantity += quantity
        cart.cost = str(product.price)
        cart.save()

    def remove(self, product):
        self.cart.remove(product)

    def get_total_price(self):
        return sum(
            Decimal(item.cost) * item.quantity for item in InsideCart.objects.filter(user_cart=self))


class InsideCart(models.Model):
    user_cart = models.ForeignKey(UserCart, on_delete=models.CASCADE)
    goods = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(verbose_name='Количество', null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость', null=True)
