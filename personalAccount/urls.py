from django.urls import path
from . import views

app_name = "personalAccount"

urlpatterns = [
    path("", views.personalAccount, name="personal"),
    path("update_profile/", views.update_profile, name="update_profile"),
    path("update_delivery_profile/", views.update_delivery_profile, name="update_delivery_profile"),
]
