from django.contrib import admin
from .models import CallBackRequest
from django.utils.html import format_html

@admin.register(CallBackRequest)
class CallBackRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'created_at', 'viewed') 
    readonly_fields = ('created_at',) 
    search_fields = ('name', 'phone')  
    ordering = ('-created_at',) 
    actions = ['mark_as_viewed']

    def mark_as_viewed(self, request, queryset):
        queryset.update(viewed=True)
    mark_as_viewed.short_description = "Mark selected requests as viewed"

    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = self.get_object(request, object_id)
        obj.viewed = True 
        obj.save()
        return super().change_view(request, object_id, form_url, extra_context)

    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        if 'name' in list_display:
            list_display = list(list_display)
            list_display[list_display.index('name')] = 'highlighted_name'
        return list_display

    def highlighted_name(self, obj):
        if not obj.viewed:
            return format_html(
                '<span style="font-weight: bold;">{}</span>',
                obj.name,
            )
        return obj.name
    highlighted_name.short_description = 'Name'

    class Media:
        js = ('deps/scripts/admin.js',)
        css = {
            'all': ('deps/style/admin.css',) 
        }
