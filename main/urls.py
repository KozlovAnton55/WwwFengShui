from django.urls import path
from main import views

app_name = "main"

urlpatterns = [
    path("", views.index, name="index"),
    path("privacyPolicy/", views.privacyPolicy, name="privacyPolicy"),
    path("qualityAssurance/", views.qualityAssurance, name="qualityAssurance"),
]
