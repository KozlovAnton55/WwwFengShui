from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Favorite
from goods.models import Products  
from django.urls import reverse

@login_required
def add_to_favorites(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id') 

        try:
            product = get_object_or_404(Products, pk=product_id)  
           
            if Favorite.objects.filter(user=request.user, product=product).exists(): 
                return JsonResponse({'status': 'error', 'message': 'Товар уже в избранном'})

            Favorite.objects.create(user=request.user, product=product)  
            return JsonResponse({'status': 'success', 'message': 'Товар добавлен в избранное'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Недопустимый метод запроса'})

@login_required
def remove_from_favorites(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')  

        try:
            product = get_object_or_404(Products, pk=product_id)  
            favorite = get_object_or_404(Favorite, user=request.user, product=product) 
            favorite.delete()
            return JsonResponse({'status': 'success', 'message': 'Удалено из избранного'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Недопустимый метод запроса'})

@login_required
def get_favorites(request):
    favorites = Favorite.objects.filter(user=request.user)
    favorite_list = []
    for favorite in favorites:
        favorite_list.append({
            'id': favorite.product.id,  
            'name': favorite.product.name,  
            'price': favorite.product.price, 
            'image': favorite.product.image.url if favorite.product.image else '',  
        })
    return JsonResponse({'favorites': favorite_list})
