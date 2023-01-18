import transliterate
from django.contrib import admin
from django.db import models
from django.db.models import Min
from django.urls import reverse
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from app_catalog.models import Product
from .singletons import SingletonModelSettings


class Category(MPTTModel):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Название')
    slug = models.SlugField(max_length=100, db_index=True, unique=True, verbose_name='url категории')
    parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name='children',
                            db_index=True, verbose_name='Родительская категория')
    icon = models.FileField(upload_to='category/', blank=True, verbose_name='Иконка')
    exec_picture = models.ImageField(blank=True, upload_to='category/', verbose_name='Изображение')

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        unique_together = [['parent', 'slug']]
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = transliterate.slugify(str(self.name))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('show_category', args=[str(self.slug)])

    def get_min(self):
        sub_categories = self.get_descendants(include_self=True)
        price = (
            Product.objects.values('price').filter(category__in=sub_categories).
            filter(available=True).aggregate(Min('price'))['price__min']
        )
        return price


class SiteSettings(SingletonModelSettings):
    cost_usual_delivery = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='обычная', help_text='Цена обычной доставки')
    cost_express_delivery = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='экспресс', help_text='Цена экспресс доставки')
    min_cost_for_free_delivery = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Минимум',
        help_text='Минимальная стоимость бесплатной доставки')
    root_category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name='Корень каталога',
        related_name='root_category', blank=True, null=True)
    category_main_page = models.ManyToManyField(
        Category, verbose_name='Категории главной страницы', default='', blank=True,
        help_text='Надо выбирать не более 3-х', db_table='app_configurations_category_main_page')
    quantity_top_product = models.PositiveIntegerField(
        verbose_name='Популярные товаров', default=8, help_text='Количество топ-товаров')
    time_cache_data = models.PositiveIntegerField(
        verbose_name='Время кэша данных', default=1, help_text='Кеш данных о товаре')

    def __str__(self):
        return 'Конфигурация'

    class Meta:
        verbose_name = "Конфигурация"
        verbose_name_plural = "Конфигурации"

    @admin.display(description='Выбранные категории')
    def show_category_main_page(self):
        list_name = (
            [category.name for category in self.category_main_page.all()] if self.category_main_page.all()
            else ['не выбрано']
        )
        return list_name
