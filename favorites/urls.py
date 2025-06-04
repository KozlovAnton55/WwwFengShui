from django.urls import path
from . import views

app_name = 'favorites'

urlpatterns = [
    path('add_to_favorites/', views.add_to_favorites, name='add_to_favorites'),
    path('remove_from_favorites/', views.remove_from_favorites, name='remove_from_favorites'),
    path('get_favorites/', views.get_favorites, name='get_favorites'),
]
