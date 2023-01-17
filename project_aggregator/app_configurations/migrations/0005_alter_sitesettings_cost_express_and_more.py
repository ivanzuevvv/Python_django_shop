# Generated by Django 4.1.3 on 2023-01-17 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_configurations', '0004_alter_sitesettings_edge_for_free_delivery_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitesettings',
            name='cost_express',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена экспресс'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='cost_usual_delivery',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена обычной'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='quantity_popular',
            field=models.PositiveIntegerField(default=8, verbose_name='Популярные товаров'),
        ),
    ]
