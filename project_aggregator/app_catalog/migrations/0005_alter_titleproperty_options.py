# Generated by Django 4.1.3 on 2023-01-16 17:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_catalog', '0004_titleproperty_alter_imageproduct_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='titleproperty',
            options={'verbose_name': 'Наименование характеристики', 'verbose_name_plural': 'Наименования характеристик'},
        ),
    ]
