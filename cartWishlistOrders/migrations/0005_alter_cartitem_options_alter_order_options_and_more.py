# Generated by Django 5.2.1 on 2025-05-22 13:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cartWishlistOrders', '0004_alter_cartitem_options_alter_order_options_and_more'),
        ('goods', '0003_products_hardware'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cartitem',
            options={'verbose_name': 'Корзина товаров', 'verbose_name_plural': 'Корзиы товаров'},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Текущий заказ', 'verbose_name_plural': 'Текущие заказы'},
        ),
        migrations.AlterModelOptions(
            name='wishlistitem',
            options={'verbose_name': 'Избранные товары', 'verbose_name_plural': 'Избранные товары'},
        ),
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Номер заказа'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pending', 'В ожидании'), ('processing', 'В обработке'), ('shipped', 'Отправлен'), ('delivered', 'Доставлен'), ('cancelled', 'Отменен')], default='pending', max_length=20),
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Количество')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='cartWishlistOrders.order', verbose_name='Заказ')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.products', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Элементы заказа',
                'verbose_name_plural': 'Элементы заказов',
            },
        ),
    ]
