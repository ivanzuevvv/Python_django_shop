# Generated by Django 4.1.3 on 2023-01-29 13:39

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_catalog', '0011_alter_product_options'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_movement_goods', '0008_alter_usercart_session'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Изменен')),
                ('city', models.CharField(max_length=100, verbose_name='Город')),
                ('address', models.CharField(max_length=250, verbose_name='Адрес')),
                ('delivery_type', models.CharField(choices=[('1', 'Обычная доставка'), ('2', 'Экспресс доставка')], default='1', max_length=1, verbose_name='Тип доставки')),
                ('payment_type', models.CharField(choices=[('1', 'Онлайн картой'), ('2', 'Онлайн со случайного чужого счета')], default='1', max_length=1, verbose_name='Тип оплаты')),
                ('card_number', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(10000000), django.core.validators.MaxValueValidator(99999999)], verbose_name='Номер карты')),
                ('delivery_price', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Цена доставки')),
                ('paid', models.BooleanField(default=False, verbose_name='оплачен')),
                ('status', models.CharField(blank=True, max_length=150, null=True, verbose_name='Ошибки оплаты')),
                ('payment_code', models.IntegerField(default=0, verbose_name='Код оплаты')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to=settings.AUTH_USER_MODEL, verbose_name='Чей заказ')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='OrderContents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='цена')),
                ('quantity', models.PositiveIntegerField(verbose_name='Количество')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='app_movement_goods.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='app_catalog.product', verbose_name='товар')),
            ],
            options={
                'verbose_name': 'Состав',
                'verbose_name_plural': 'Составы',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='structure',
            field=models.ManyToManyField(related_name='order', through='app_movement_goods.OrderContents', to='app_catalog.product', verbose_name='Содержание заказа'),
        ),
    ]
