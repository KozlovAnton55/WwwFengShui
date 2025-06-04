from django.urls import path
from . import views

app_name = 'cartWishlistOrders'

urlpatterns = [
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('get_cart_data/', views.get_cart_data, name='get_cart_data'),
    path('get_wishlist_data/', views.get_wishlist_data, name='get_wishlist_data'),
    path('process_order/', views.process_order, name='process_order'),
    path('get_current_orders/', views.get_current_orders, name='get_current_orders'),
    path('update_cart_item_quantity/<int:product_id>/', views.update_cart_item_quantity, name='update_cart_item_quantity'),
]