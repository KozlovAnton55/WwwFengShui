from django.shortcuts import render
from reviews.models import Review
from goods.models import Categories

def index(request):
    message = request.GET.get('message', '')  
    approved_reviews = Review.objects.filter(is_published=True).order_by('-created_at')
    categories = Categories.objects.all() 
    context = {
        'title': '--Главная Feng-Shui--',
        'approved_reviews': approved_reviews,
        'categories': categories,  
        'message': message,  
    }
    return render(request, 'main/index.html', context)

def privacyPolicy(request):
    context: dict[str, str] = {
        'title': '--Политика Конфиденциальности--',
    }
    return render(request, "main/privacyPolicy.html", context)

def qualityAssurance(request):
    context: dict[str, str] = {
        'title': '--Гарантии качества--',
    }
    return render(request, "main/qualityAssurance.html", context)