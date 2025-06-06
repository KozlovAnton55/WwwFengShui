# Generated by Django 5.2.1 on 2025-05-16 13:27

import django.db.models.deletion
import jsonfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Название категории')),
                ('slug', models.SlugField(blank=True, max_length=200, unique=True, verbose_name='Слаг')),
                ('image', models.ImageField(blank=True, null=True, upload_to='category_images/', verbose_name='Изображение категории')),
            ],
            options={
                'verbose_name': 'категорию',
                'verbose_name_plural': 'Категории',
                'db_table': 'category',
            },
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название товара')),
                ('slug', models.SlugField(blank=True, max_length=200, unique=True, verbose_name='Слаг')),
                ('characteristics', jsonfield.fields.JSONField(blank=True, null=True, verbose_name='Характеристики')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')),
                ('image', models.ImageField(blank=True, null=True, upload_to='products/', verbose_name='Изображение товара')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.categories', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'товар',
                'verbose_name_plural': 'Товары',
                'db_table': 'product',
            },
        ),
    ]
