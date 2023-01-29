from decimal import Decimal

from django.conf import settings
from django.contrib import admin
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from app_catalog.models import Product


class UserCart(models.Model):
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='cart', verbose_name='Чья корзина', blank=True, null=True)
    session = models.CharField(
        verbose_name='Сессия', default='', max_length=40)
    cart = models.ManyToManyField(
        Product, through='InsideCart', verbose_name='Содержание корзины',
        related_name="carts", blank=True)

    def __str__(self):
        return 'Корзина ' + str(self.owner.email) if self.owner else 'Корзина Anonymous'

    def __len__(self):
        return sum(item.quantity for item in self.contents.only('quantity').all())

    def __iter__(self):
        for item in self.contents.all():
            data = {
                'total_price': item.cost * item.quantity,
                'product': item.product,
                'quantity': item.quantity,
                'price': item.cost,
            }
            yield data

    def add(self, product, quantity=1, update_quantity=False):
        cart = self.contents.get_or_create(user_cart=self, product=product)[0]
        if update_quantity:
            cart.quantity = quantity
        else:
            cart.quantity += quantity
        cart.cost = str(product.price)
        cart.save()

    def add_cart(self, cart):
        if cart:
            for goods in cart.contents.all():
                self.add(goods.product, goods.quantity)
            cart.clear()

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
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товары')
    quantity = models.PositiveSmallIntegerField(verbose_name='Количество', default=0)
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость', null=True)

    def __str__(self):
        return f'{self.product}={self.quantity} шт.'

    def save(self, *args, **kwargs):
        self.cost = str(self.product.price)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class Order(models.Model):
    DELIVERY_CHOICES = (
        ("1", "Обычная доставка"),
        ("2", "Экспресс доставка"),)

    PAYMENT_CHOICES = (
        ("1", "Онлайн картой"),
        ("2", "Онлайн со случайного чужого счета"),)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Изменен')
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='order', on_delete=models.CASCADE, verbose_name='Чей заказ')
    city = models.CharField(max_length=100, verbose_name='Город')
    address = models.CharField(max_length=250, verbose_name='Адрес')
    delivery_type = models.CharField(
        max_length=1, choices=DELIVERY_CHOICES, verbose_name='Тип доставки', default="1")
    payment_type = models.CharField(
        max_length=1, choices=PAYMENT_CHOICES, verbose_name='Тип оплаты', default="1")
    card_number = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(10000000), MaxValueValidator(99999999)], verbose_name='Номер карты')
    delivery_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена доставки', default=0)
    paid = models.BooleanField(default=False, verbose_name='оплачен')
    status = models.CharField(max_length=150, verbose_name='Ошибки оплаты', blank=True, null=True)
    payment_code = models.IntegerField(default=0, verbose_name='Код оплаты')
    structure = models.ManyToManyField(
        Product, through='OrderContents', verbose_name='Содержание заказа', related_name='order')

    class Meta:
        ordering = ('-created_at',)
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f'Заказ {self.owner.email} №{self.id} от {self.created_at.strftime("%d-%m-%Y")}'

    @admin.display(description='Стоимость заказа')
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all()) + self.delivery_price


class OrderContents(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE, verbose_name='товар')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='цена')
    quantity = models.PositiveIntegerField(verbose_name='Количество')

    def __str__(self):
        return f'{self.product}={self.quantity} шт.'

    def get_cost(self):
        return self.price * self.quantity

    def save(self, *args, **kwargs):
        self.price = str(self.product.price)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Содержание"
        verbose_name_plural = "Составы"
