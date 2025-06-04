"""
URL configuration for WwwFengShui project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main.urls", namespace="main")),
    path("callBack/", include("callBack.urls", namespace="callBack")),
    path("categories/", include("goods.urls", namespace="goods")),
    path("delivery/", include("delivery.urls", namespace="delivery")),
    path("ourPromotions/", include("ourPromotions.urls", namespace="ourPromotions")),
    path(
        "personalAccount/", include("personalAccount.urls", namespace="personalAccount")
    ),
    path("reviews/", include("reviews.urls", namespace="reviews")),
    path(
        "cartWishlistOrders/",
        include("cartWishlistOrders.urls", namespace="cartWishlistOrders"),
    ),
    path("user/", include("users.urls", namespace="user")),
    path("search/", include("search.urls", namespace="search"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
