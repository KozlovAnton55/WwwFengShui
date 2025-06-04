from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from users.models import UserProfile
from django.contrib import messages
from reviews.models import Review
from django.contrib.auth import login
from .models import DeliveryProfile
from .forms import DeliveryProfileForm
from django.core.serializers import serialize 
from django.http import JsonResponse
import json 


@login_required
def personalAccount(request):
    user_reviews = Review.objects.filter(
        author=request.user, is_published=True
    ).order_by("-created_at")
    try:
        user_profile = request.user.profile
        phone = user_profile.phone
    except UserProfile.DoesNotExist:
        phone = None

    delivery_profile, created = DeliveryProfile.objects.get_or_create(user=request.user)

    delivery_profile_json = serialize('json', [delivery_profile], fields=('city', 'street', 'house', 'entrance', 'floor'))

    import json
    delivery_profile_data = json.loads(delivery_profile_json)[0]['fields']

    context = {
        "approved_reviews": user_reviews,
        "title": "Личный кабинет",
        "phone": phone,
        "delivery_profile": delivery_profile,  
        "delivery_profile_data": delivery_profile_data,  
    }
    return render(request, "personalAccount/personalAccount.html", context)


@login_required
def update_profile(request):
    if request.method == "POST":
        nickname = request.POST.get("nickname")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        try:
            user_profile = request.user.profile
        except UserProfile.DoesNotExist:
            user_profile = UserProfile(user=request.user)

        user_profile.phone = phone
        user_profile.save()

        if not nickname:
            nickname = request.user.username

        request.user.username = nickname
        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.save()

        if password:
            request.user.set_password(password)
            request.user.save()

            login(request, request.user)

        messages.success(request, "Профиль успешно обновлен!")
        return redirect("personalAccount:personal")

    return redirect("personalAccount:personal")


@login_required
def update_delivery_profile(request):
    if request.method == "POST":
        delivery_profile, created = DeliveryProfile.objects.get_or_create(user=request.user)
        form = DeliveryProfileForm(request.POST, instance=delivery_profile)
        if form.is_valid():
            form.save()  
            messages.success(request, "Профиль доставки успешно обновлен!")
            return redirect("personalAccount:personal")
        else:
            messages.error(request, "Ошибка при обновлении профиля доставки. Пожалуйста, проверьте данные.")
            print(form.errors)
    else:
        return redirect("personalAccount:personal")
    return redirect("personalAccount:personal")
