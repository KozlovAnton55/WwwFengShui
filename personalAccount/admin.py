from django.contrib import admin
from .models import DeliveryProfile


@admin.register(DeliveryProfile)
class DeliveryProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'city', 'street', 'house', 'entrance', 'floor', 'needs_elevator']  
    list_filter = ['city', 'needs_elevator']  
    search_fields = ['city', 'street', 'house', 'user__username', 'user__email']
