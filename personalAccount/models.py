from django.db import models
from django.contrib.auth.models import User

class DeliveryProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='delivery_profile')
    city = models.CharField(max_length=100, verbose_name="Город", default="")
    street = models.CharField(max_length=100, verbose_name="Улица", blank=True, null=True)
    house = models.CharField(max_length=20, verbose_name="Дом", blank=True, null=True)
    entrance = models.CharField(max_length=10, verbose_name="Подъезд", blank=True, null=True)
    floor = models.IntegerField(verbose_name="Этаж", blank=True, null=True, default=1)
    needs_elevator = models.BooleanField(verbose_name="Нужен ли подъем", default=False)
    has_lift = models.BooleanField(verbose_name="Наличие лифта", default=False)  

    def __str__(self):
        return f"Delivery profile for {self.user.username}"
    
    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили доставки"
