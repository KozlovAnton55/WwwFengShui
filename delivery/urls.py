from django.urls import path
from delivery import views

app_name = "delivery"

urlpatterns = [
    path("", views.delivery, name="delivery"),
    path("api/pricing/", views.get_delivery_pricing, name="get_delivery_pricing"),
    path("calculate_delivery_cost/", views.calculate_delivery_cost_view, name="calculate_delivery_cost"),
]
