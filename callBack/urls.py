from django.urls import path

from callBack import views

app_name = "callBack"

urlpatterns = [
    path("", views.callBack, name="callBack"),
    path(
        "admin/callback/callbackrequest/recent_count/",
        views.recent_callback_count,
        name="recent_callback_count",
    ),
]
