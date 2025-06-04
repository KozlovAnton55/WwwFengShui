from django.shortcuts import render
from .models import Promotion


def ourPromotions_view(request):
    promotions = Promotion.objects.all()
    context = {
        "promotions": promotions,
        "title": "Наши Акции", 
    }
    return render(request, "ourPromotions/ourPromotions.html", context)
