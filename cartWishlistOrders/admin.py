from django.contrib import admin
from .models import CartItem, WishlistItem, Order, OrderItem
from django.utils.html import format_html
from django.contrib import messages


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'total_price') 
    search_fields = ('user__username', 'product__name') 
    readonly_fields = ('user', 'product', 'quantity', 'total_price') 

    def total_price(self, obj):
        return format_html("<b>{}</b>", obj.total_price())

    total_price.short_description = 'Общая стоимость'
    total_price.admin_order_field = 'product__price' 

    def save_model(self, request, obj, form, change):
        
        if change:  
            messages.warning(request, "Редактирование корзины через админ-панель запрещено.")
            return  
        super().save_model(request, obj, form, change)

class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product') 
    search_fields = ('user__username', 'product__name')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price')
    can_delete = False

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'order_number', 'delivery_address', 'total_amount', 'status', 'created_at')
    search_fields = ('user__username', 'order_number')
    readonly_fields = ('order_number', 'created_at', 'total_amount')
    list_filter = ('status',)
    inlines = [OrderItemInline]

admin.site.register(CartItem, CartItemAdmin)
admin.site.register(WishlistItem, WishlistItemAdmin)
admin.site.register(Order, OrderAdmin)