from django.shortcuts import render, get_object_or_404
from .models import Categories, Products

def categories(request):
    categories = Categories.objects.all()
    context = {
        "title": "--Категории товаров--",
        "categories": categories,
    }
    return render(request, "goods/categories.html", context)

def category(request, category_slug):  
    category = get_object_or_404(Categories, slug=category_slug)
    products = Products.objects.filter(category=category)
    context = {
        "title": f"Категория: {category.name}",
        "category_name": category.name,
        "products": products,
        "category": category,  
    }
    return render(request, "goods/category.html", context)