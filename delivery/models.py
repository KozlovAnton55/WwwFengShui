from django.db import models


class DeliveryPricing(models.Model):
    zone_1_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Зона доставки 20км"
    )
    zone_2_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Зона доставки 40км"
    )
    price_per_floor_with_lift = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Стоимость подъема за этаж с лифтом",
    )
    price_per_floor_without_lift = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Стоимость подъема за этаж без лифта",
    )
    heavy_furniture_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Стоимость доставки тяжелой мебели",
    )
    light_furniture_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Стоимость доставки легкой мебели"
    )

    def __str__(self):
        return f"Pricing: Zone 1 - {self.zone_1_price}, Zone 2 - {self.zone_2_price}"

    class Meta:
        verbose_name = "Параметр"
        verbose_name_plural = "Параметры стоимости"