import transliterate
from django.db import models
from django.urls import reverse


class Product(models.Model):
    # category = models.ForeignKey('app_configurations.Category', on_delete=models.CASCADE, related_name='products', blank=True)
    type_device = models.CharField(max_length=50, verbose_name='Тип устройства')
    fabricator = models.CharField(max_length=100, verbose_name='Производитель')
    model = models.CharField(max_length=100, verbose_name='Модель')
    slug = models.SlugField(max_length=255, null=False, unique=True, verbose_name="URL товара")
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    stock = models.PositiveIntegerField(verbose_name='В наличии')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    available = models.BooleanField(default=True, verbose_name='В продаже')
    limited = models.BooleanField(default=True, verbose_name='Ограниченная серия')
    properties = models.ManyToManyField('PropertyProduct', related_name='products')

    def __str__(self):
        return f'{self.type_device} {self.fabricator}'

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.pk, self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = transliterate.slugify(f'{self.type_device} {self.model} {self.model}')
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ['price']
        index_together = ['slug']
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class ImageProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/%Y/%m/%d')


class PropertyProduct(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    value = models.CharField(max_length=255, verbose_name='Значение характеристики')

    def __str__(self):
        return f'{self.title}={self.value}'
