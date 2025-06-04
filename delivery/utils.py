from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from django.conf import settings
from functools import lru_cache
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from .models import DeliveryPricing


@lru_cache(maxsize=128)
def geocode_city(city):
    """
    Функция для геокодирования города (получения координат по названию города).
    """
    geolocator = Nominatim(user_agent="delivery_app")
    try:
        location = geolocator.geocode(city, timeout=5)
        if location is None:
            raise ValueError(f"Не удалось найти координаты города: {city}")
        return (location.latitude, location.longitude)
    except GeocoderTimedOut:
        raise TimeoutError(
            f"Превышено время ожидания геокодирования для города: {city}"
        )
    except GeocoderUnavailable:
        raise ConnectionError(f"Сервис геокодирования недоступен для города: {city}")
    except Exception as e:
        raise ValueError(f"Ошибка геокодирования для города {city}: {e}")


def calculate_delivery_cost(city, floor=1, needs_elevator=False, has_lift=False):
    """
    Функция для расчета стоимости доставки.
    """
    try:
        city_coordinates = geocode_city(city)

        center_coordinates = (
            settings.DELIVERY_CENTER_LAT,
            settings.DELIVERY_CENTER_LON,
        )

        if center_coordinates is None or city_coordinates is None:
            raise ValueError(
                "Не удалось получить координаты для расчета стоимости доставки"
            )

        distance = geodesic(center_coordinates, city_coordinates).km

        # Получаем данные о ценах из базы данных
        try:
            pricing = DeliveryPricing.objects.first()
            if not pricing:
                raise ValueError("В базе данных отсутствуют данные о ценах")
        except DeliveryPricing.DoesNotExist:
            raise ValueError("В базе данных отсутствуют данные о ценах")

        delivery_cost = "Не доставляется"
        if distance <= 20:
            delivery_cost = float(pricing.zone_1_price)
        elif distance <= 40:
            delivery_cost = float(pricing.zone_2_price)

        if needs_elevator and floor > 1 and delivery_cost != "Не доставляется":
            if has_lift:
                delivery_cost += float(pricing.price_per_floor_with_lift) * (floor - 1)
            else:
                delivery_cost += float(pricing.price_per_floor_without_lift) * (
                    floor - 1
                )

        return delivery_cost
    except TimeoutError as e:
        raise
    except (ValueError, ConnectionError) as e:
        raise
