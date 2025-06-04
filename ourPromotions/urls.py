from django.urls import path
from ourPromotions import views

app_name = "ourPromotions"

urlpatterns = [
    path("", views.ourPromotions_view, name="ourPromotions"),
]
