# delivery/admin.py
from django.contrib import admin
from .models import DeliveryPricing

@admin.register(DeliveryPricing)
class DeliveryPricingAdmin(admin.ModelAdmin):
    list_display = (
        'zone_1_price',
        'zone_2_price',
        'price_per_floor_with_lift',
        'price_per_floor_without_lift',
        'heavy_furniture_price',
        'light_furniture_price',
    )
    search_fields = ('zone_1_price', 'zone_2_price', 'price_per_floor_with_lift', 'price_per_floor_without_lift')
