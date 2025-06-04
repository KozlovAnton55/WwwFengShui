from django.db import models
from goods.models import Products

class Promotion(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name="Товар")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    image = models.ImageField(upload_to='promotions/', blank=True, null=True, verbose_name="Изображение")
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Уцененная цена")

    def __str__(self):
        return self.product.name  

    class Meta:
        db_table = "Promotion"
        verbose_name = "Акцию"
        verbose_name_plural = "Товары по Акции"