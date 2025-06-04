from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import CartItem, WishlistItem, Order, OrderItem
from goods.models import Products
import uuid
from django.conf import settings 
from delivery.utils import calculate_delivery_cost  

@login_required
def add_to_cart(request, product_id):
    """Добавление товара в корзину."""
    product = get_object_or_404(Products, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user, product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return JsonResponse(
        {"status": "success", "cart_items_count": request.user.cart_items.count()}
    )


@login_required
def remove_from_cart(request, product_id):
    """Удаление товара из корзины."""
    product = get_object_or_404(Products, id=product_id)
    try:
        cart_item = CartItem.objects.get(user=request.user, product=product)
        cart_item.delete()
        return JsonResponse(
            {"status": "success", "cart_items_count": request.user.cart_items.count()}
        )
    except CartItem.DoesNotExist:
        return JsonResponse(
            {"status": "error", "message": "Товар не найден в корзине"}, status=404
        )


@login_required
def add_to_wishlist(request, product_id):
    """Добавление товара в избранное."""
    product = get_object_or_404(Products, id=product_id)
    WishlistItem.objects.get_or_create(user=request.user, product=product)
    return JsonResponse(
        {
            "status": "success",
            "wishlist_items_count": request.user.wishlist_items.count(),
        }
    )


@login_required
def remove_from_wishlist(request, product_id):
    """Удаление товара из избранного."""
    product = get_object_or_404(Products, id=product_id)
    try:
        wishlist_item = WishlistItem.objects.get(user=request.user, product=product)
        wishlist_item.delete()
        return JsonResponse(
            {
                "status": "success",
                "wishlist_items_count": request.user.wishlist_items.count(),
            }
        )
    except WishlistItem.DoesNotExist:
        return JsonResponse(
            {"status": "error", "message": "Товар не найден в избранном"}, status=404
        )


@login_required
def get_cart_data(request):
    """Получение данных о корзине (кол-во товаров, общая стоимость)."""
    cart_items = request.user.cart_items.all()
    cart_items_data = []
    for item in cart_items:
        cart_items_data.append({
            'product': {
                'id': item.product.id,
                'name': item.product.name,
                'price': str(item.product.price),
                'image': item.product.image.url if item.product.image else '',
            },
            'quantity': item.quantity,
        })
    cart_items_count = cart_items.count()
    total_price = sum(item.total_price() for item in cart_items)
    print(f"total_price: {total_price}") 

   
    delivery_address = ""
    delivery_cost = "Не рассчитано"
    try:
        delivery_profile = request.user.delivery_profile
        city = delivery_profile.city
        floor = delivery_profile.floor
        needs_elevator = delivery_profile.needs_elevator
        has_lift = delivery_profile.has_lift
        delivery_address = f"Город: {city}, Улица: {delivery_profile.street or ''}, Дом: {delivery_profile.house or ''}, Подъезд: {delivery_profile.entrance or ''}, Этаж: {floor or ''}"
        print(f"delivery_address: {delivery_address}")  

        if city:
            try:
                delivery_cost = calculate_delivery_cost(city=city, floor=floor, needs_elevator=needs_elevator, has_lift=has_lift)
                print(f"delivery_cost: {delivery_cost}")  
                if isinstance(delivery_cost, float):
                    delivery_cost = f"{delivery_cost:.2f}" 
            except Exception as e:
                print(f"Ошибка при расчете стоимости доставки: {e}") 
                delivery_cost = "Ошибка" 
        else:
            print("Город доставки не указан в профиле")
    except Exception as e:
        print(f"Ошибка при получении данных профиля: {e}") 
        delivery_cost = "Не рассчитано" 


    try:
        total_order_cost = float(total_price)
        print(f"total_order_cost (before adding delivery): {total_order_cost}")  
        if delivery_cost != "Не рассчитано" and delivery_cost != "Ошибка": 
            try:
                delivery_cost_float = float(delivery_cost) 
                total_order_cost += delivery_cost_float
            except ValueError:
                print("Не удалось преобразовать delivery_cost в float") 
               
        print(f"total_order_cost (after adding delivery): {total_order_cost}")  
        total_order_cost_str = f"{total_order_cost:.2f}" 
    except ValueError:
        print("Не удалось преобразовать total_price в float")  
        total_order_cost_str = str(total_price) 

    return JsonResponse({
        'cart_items_count': cart_items_count,
        'total_price': str(total_price),
        'cart_items': cart_items_data,
        'delivery_address': delivery_address,
        'delivery_cost': delivery_cost,
        'total_order_cost': total_order_cost_str,
    })


@login_required
def get_wishlist_data(request):
    """Получение данных об избранном (кол-во товаров)."""
    wishlist_items = request.user.wishlist_items.all()
    wishlist_items_data = []
    for item in wishlist_items:
        wishlist_items_data.append(
            {
                "product": {
                    "id": item.product.id,
                    "name": item.product.name,
                    "price": str(item.product.price),
                    "image": item.product.image.url if item.product.image else "",
                },
            }
        )
    wishlist_items_count = wishlist_items.count()
    return JsonResponse(
        {
            "wishlist_items_count": wishlist_items_count,
            "wishlist_items": wishlist_items_data,
        }
    )


@login_required
def process_order(request):
    """Обработка оформления заказа."""
    delivery_address = request.POST.get("delivery_address", "")
    order_number = str(uuid.uuid4()).upper()[:8]
    total_amount = sum(item.total_price() for item in request.user.cart_items.all()) 

    
    try:
        delivery_profile = request.user.delivery_profile
        
        delivery_address = f"Город: {delivery_profile.city}, Улица: {delivery_profile.street or ''}, Дом: {delivery_profile.house or ''}, Подъезд: {delivery_profile.entrance or ''}, Этаж: {delivery_profile.floor or ''}"

      
        from delivery.utils import calculate_delivery_cost
        delivery_cost = calculate_delivery_cost(city=delivery_profile.city, floor=delivery_profile.floor, needs_elevator=delivery_profile.needs_elevator, has_lift=delivery_profile.has_lift)
        if isinstance(delivery_cost, float):
            total_amount = float(total_amount) + delivery_cost 
    except:
        pass  

    order = Order.objects.create(
        user=request.user,
        order_number=order_number,
        delivery_address=delivery_address,
        total_amount=total_amount, 
    )

    for cart_item in request.user.cart_items.all():
        OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            quantity=cart_item.quantity,
            price=cart_item.product.price,
        )

    request.user.cart_items.all().delete()

    return JsonResponse({"status": "success", "order_number": order_number})


@login_required
def get_current_orders(request):
    """Получение текущих заказов пользователя."""
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    orders_data = []
    for order in orders:
        orders_data.append(
            {
                "order_number": order.order_number,
                "created_at": order.created_at.strftime("%d.%m.%Y %H:%M"),
                "delivery_address": order.delivery_address,
                "total_amount": str(order.total_amount),
                "status": order.get_status_display(),
                "total_order_cost": str(order.total_amount), 
            }
        )
    return JsonResponse({"orders": orders_data})


@login_required
@require_POST
def update_cart_item_quantity(request, product_id):
    """Обновление количества товара в корзине."""
    try:
        quantity = int(request.POST.get("quantity"))
        if quantity <= 0:
            return JsonResponse(
                {"status": "error", "message": "Количество должно быть больше 0"}
            )

        cart_item = get_object_or_404(
            CartItem, user=request.user, product_id=product_id
        )
        cart_item.quantity = quantity
        cart_item.save()
        return JsonResponse({"status": "success"})
    except ValueError:
        return JsonResponse({"status": "error", "message": "Неверное количество"})
    except CartItem.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Товар не найден в корзине"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})