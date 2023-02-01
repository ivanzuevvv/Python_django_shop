import transliterate
from django.contrib import admin
from django.db import models
from django.urls import reverse
from mptt.fields import TreeForeignKey


class Product(models.Model):
    category = TreeForeignKey(
        'app_configurations.Category', on_delete=models.PROTECT,
        related_name='products', verbose_name="Категория товара")
    type_device = models.CharField(max_length=50, verbose_name='Тип устройства', default='')
    fabricator = models.CharField(max_length=100, verbose_name='Производитель', default='')
    model = models.CharField(max_length=100, verbose_name='Модель', default='')
    slug = models.SlugField(max_length=255, null=False, unique=True, verbose_name="URL товара", default='')
    description = models.TextField(blank=True, verbose_name='Описание', default='')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена', default=0)
    stock = models.PositiveIntegerField(verbose_name='В наличии', default=0)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    available = models.BooleanField(default=True, verbose_name='В продаже')
    limited = models.BooleanField(default=False, verbose_name='Ограниченная серия')
    extra_data = models.ManyToManyField("TitleData", through='ExtraData', verbose_name='Дополнительные данные')
    options = models.ManyToManyField('TitleProperty', through='PropertyProduct')

    def __str__(self):
        return f'{self.type_device} {self.fabricator} {self.model}'

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.slug])

    @property
    @admin.display(description='Наименование')
    def get_full_name(self):
        return f'{self.type_device} {self.fabricator} {self.model}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = transliterate.slugify(f'{self.type_device} {self.model} {self.model}')
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ['price']
        index_together = ['slug']
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class TitleData(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Наименование"
        verbose_name_plural = "Наименования"


class ValueData(models.Model):
    value = models.CharField(max_length=100, verbose_name='Заголовок')

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = "Значение"
        verbose_name_plural = "Значения"


class ExtraData(models.Model):
    title = models.ForeignKey(TitleData, related_name='extradata', on_delete=models.CASCADE, verbose_name="Параметр")
    device = models.ForeignKey(
        Product, related_name='extradata', on_delete=models.CASCADE, verbose_name='Устройство', db_index=True,)
    value = models.ForeignKey(ValueData, related_name='extradata', on_delete=models.CASCADE, verbose_name="Значение")

    def __str__(self):
        return f'{self.title}: {self.value}'

    class Meta:
        verbose_name = "Дополнительные данные"
        verbose_name_plural = "Сведения"


class ImageProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/%Y/%m/%d', verbose_name="миниатюры")

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"


class TitleProperty(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Свойство"
        verbose_name_plural = "Свойства"


class PropertyProduct(models.Model):
    title = models.ForeignKey(TitleProperty, on_delete=models.CASCADE, verbose_name='Заголовок')
    device = models.ForeignKey(
        Product, related_name='properties', on_delete=models.CASCADE, verbose_name='Устройство', db_index=True,
    )
    value = models.CharField(max_length=255, verbose_name='Значение характеристики')

    def __str__(self):
        return f'{self.title}={self.value}'

    class Meta:
        verbose_name = "Характеристики"
        verbose_name_plural = "Характеристики"
