from django.urls import path
from . import views

app_name = "reviews"

urlpatterns = [
    path("submit_review/", views.submit_review, name="submit_review"),
]
