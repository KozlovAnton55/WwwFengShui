from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from goods.models import Products, Categories
from django.urls import reverse

def search_products(request):
    query = request.GET.get("q")

    if not query:
        message = "Введите запрос для поиска."
        return redirect(reverse('main:index') + f'?message={message}')

    try:
        products = Products.objects.filter(
            Q(category__name__icontains=query) | Q(name__icontains=query)
        )

        if products.exists():
            first_product = products.first()
            category = first_product.category
            return redirect("goods:category", category_slug=category.slug)
        else:
            message = "Таких товаров нет у нас в каталоге."
            return redirect(reverse('main:index') + f'?message={message}')

    except Exception as e:
        message = "Произошла ошибка при поиске."
        return redirect(reverse('main:index') + f'?message={message}')
