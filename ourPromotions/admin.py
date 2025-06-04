from django.contrib import admin
from .models import Promotion


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "discounted_price",
        "old_price",
    )
    readonly_fields = ("old_price",)

    fieldsets = (
        ("Основная информация", {"fields": ("product", "description", "image")}),
        (
            "Цена",
            {
                "fields": (
                    "old_price",
                    "discounted_price",
                )  
            },
        ),
    )

    def old_price(self, obj):
        return obj.product.price  

    old_price.short_description = "Старая цена"  

    def save_model(self, request, obj, form, change):
        if not obj.image:
            obj.image = obj.product.image
        super().save_model(request, obj, form, change)
