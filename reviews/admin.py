from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'created_at', 'is_published') 
    list_filter = ('is_published', 'author')
    search_fields = ('text', 'author__username')
    readonly_fields = ('author', 'created_at')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return True
