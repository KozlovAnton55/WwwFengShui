from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import DeliveryPricing
from .utils import calculate_delivery_cost 

def delivery(request):
    context = {
        'title': '--Калькулятор Доставки--',
    }
    return render(request, 'delivery/delivery.html', context)

def get_delivery_pricing(request):
    try:
        pricing = DeliveryPricing.objects.first()
        print("Pricing object:", pricing) 
        if pricing:
            data = {
                'zone_1_price': str(pricing.zone_1_price),  
                'zone_2_price': str(pricing.zone_2_price),  
                'price_per_floor_with_lift': str(pricing.price_per_floor_with_lift),
                'price_per_floor_without_lift': str(pricing.price_per_floor_without_lift),
                'heavy_furniture_price': str(pricing.heavy_furniture_price),
                'light_furniture_price': str(pricing.light_furniture_price),
            }
            print("Pricing data:", data) 
            return JsonResponse(data)
        else:
            print("No pricing data found") 
            return JsonResponse({'error': 'No pricing data available'}, status=404)
    except Exception as e:
        print("Error:", str(e)) 
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def calculate_delivery_cost_view(request):
    if request.method == 'POST':
        city = request.POST.get('city')
        floor = int(request.POST.get('floor', 1))
        needs_elevator = request.POST.get('needs_elevator') == 'true'
        has_lift = request.POST.get('has_lift') == 'true' 

        if not city:
            return JsonResponse({'error': 'Не указан город'}, status=400)

        try:
            delivery_cost = calculate_delivery_cost(city, floor, needs_elevator, has_lift)  
            return JsonResponse({'delivery_cost': delivery_cost})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Только POST-запросы'}, status=405)