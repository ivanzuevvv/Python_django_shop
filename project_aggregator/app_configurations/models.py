import transliterate
from django.db import models
from django.db.models import Min
from django.urls import reverse
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from app_catalog.models import Product


class Category(MPTTModel):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Название')
    slug = models.SlugField(max_length=100, db_index=True, unique=True, verbose_name='url категории')
    parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name='children',
                            db_index=True, verbose_name='Родительская категория')
    icon = models.FileField(upload_to='category/', blank=True, verbose_name='Иконка')
    exec_picture = models.ImageField(blank=True, upload_to='category/', verbose_name='Изображение')

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        unique_together = [['parent', 'slug']]
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = transliterate.slugify(self.name)
        super().save(*args, **kwargs)

    # def get_absolute_url(self):
    #     return reverse('product-by-category', args=[str(self.slug)])

    # def get_min(self):
    #     sub_categories = self.get_descendants(include_self=True)
    #     price = Product.objects.values('price').filter(category__in=sub_categories).filter(available=True).aggregate(
    #         Min('price'))['price__min']
    #     return price

    def __str__(self):
        return self.name
