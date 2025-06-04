from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import Categories, Products


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'category', 'article') 

    def save_model(self, request, obj, form, change):
        try:
            obj.full_clean() 
            super().save_model(request, obj, form, change)
        except ValidationError as e:
            form.errors['__all__'] = e.messages 
            self.message_user(request, f"Ошибка валидации: {e}", level='error') 


