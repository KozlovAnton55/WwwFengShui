from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
from .models import UserProfile


@csrf_protect
def registration_view(request):
    if request.method == "POST":
        try:
            first_name = request.POST.get("registerFirstName")
            last_name = request.POST.get("registerLastName")
            phone = request.POST.get("registerPhone")
            email = request.POST.get("registerEmail")
            password = request.POST.get("registerPassword")
            password2 = request.POST.get("registerPassword2")
            nickname = request.POST.get("registerNickname")

            if not (
                first_name
                and last_name
                and phone
                and email
                and password
                and password2
                and nickname
            ):
                return JsonResponse(
                    {"status": "error", "message": "Пожалуйста, заполните все поля."}
                )

            if password != password2:
                return JsonResponse(
                    {"status": "error", "message": "Пароли не совпадают."}
                )

            if User.objects.filter(username=nickname).exists():  
                return JsonResponse(
                    {
                        "status": "error",
                        "message": "Пользователь с таким никнеймом уже существует.",
                    }
                )

            try:
                user = User.objects.create_user(
                    username=nickname, 
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                )
                user.save()
                user_profile = UserProfile(user=user, phone=phone)
                user_profile.save()

            except Exception as e:
                return JsonResponse(
                    {"status": "error", "message": f"Что-то пошло не так!"}
                )

            user = authenticate(request, username=nickname, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse(
                    {
                        "status": "success",
                        "message": "Вы успешно прошли регистрацию и теперь авторизованы в системе!",
                    }
                )
            else:
                return JsonResponse(
                    {"status": "error", "message": "Что-то пошло не так!"}
                )
        except KeyError as e:
            return JsonResponse({"status": "error", "message": "Что-то пошло не так!"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": "Что-то пошло не так!"})
    else:
        return JsonResponse(
            {"status": "error", "message": "Недопустимый метод запроса."}
        )


@csrf_protect
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("authName")
        password = request.POST.get("authPassword")

        if not (username and password):
            return JsonResponse(
                {"status": "error", "message": "Пожалуйста, заполните все поля."}
            )

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse(
                {
                    "status": "success",
                    "message": f"Поздравляем, {username}, вы успешно авторизовались в системе!",
                }
            )
        else:
            return JsonResponse(
                {"status": "error", "message": "Неверное имя пользователя или пароль."}
            )
    else:
        return JsonResponse(
            {"status": "error", "message": "Недопустимый метод запроса."}
        )


def logout_view(request):
    logout(request)
    return redirect("main:index")


@login_required
def get_wishlist_data(request):
    return JsonResponse({"wishlist": []})


@login_required
def get_cart_data(request):
    return JsonResponse({"cart": []})


@login_required
def get_current_orders(request):
    return JsonResponse({"orders": []})
