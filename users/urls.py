from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("registration/", views.registration_view, name="registration"),
    path("logout/", views.logout_view, name="logout"), 
    path("get_wishlist_data/", views.get_wishlist_data, name="get_wishlist_data"),
    path("get_cart_data/", views.get_cart_data, name="get_cart_data"),
    path("get_current_orders/", views.get_current_orders, name="get_current_orders"),
]