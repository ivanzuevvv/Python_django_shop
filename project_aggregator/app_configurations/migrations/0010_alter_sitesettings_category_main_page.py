# Generated by Django 4.1.3 on 2023-01-17 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_configurations', '0009_alter_sitesettings_category_main_page'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitesettings',
            name='category_main_page',
            field=models.ManyToManyField(blank=True, db_table='app_configurations_category_main_page', default='', help_text='Надо выбирать не более 3-х', to='app_configurations.category', verbose_name='Категории главной страницы'),
        ),
    ]
