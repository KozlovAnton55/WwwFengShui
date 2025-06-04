from django.shortcuts import render
from django.http import JsonResponse
from .models import CallBackRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required


@csrf_exempt 
def callBack(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        if name and phone:  
            CallBackRequest.objects.create(name=name, phone=phone, message=message)
            return JsonResponse({"status": "success"})
        else:
            return JsonResponse(
                {"status": "error", "message": "Имя и телефон обязательны."}, status=400
            )

    context = {
        "title": "--Заказать Звонок--",
    }
    return render(request, "callBack/callBack.html", context)


@staff_member_required
def recent_callback_count(request):
    count = CallBackRequest.objects.filter(
        viewed=False
    ).count() 
    return JsonResponse({"count": count})