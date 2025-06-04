from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Review
from django.contrib import messages
from django.urls import reverse


@login_required
def submit_review(request):
    if request.method == "POST":
        review_text = request.POST.get("reviewText")
        rating = int(request.POST.get("rating"))

        if review_text:
            review = Review(
                text=review_text, author=request.user, rating=rating
            ) 
            review.save()
            messages.success(request, "Ваш отзыв успешно отправлен на модерацию.")
        else:
            messages.error(request, "Пожалуйста, заполните текст отзыва.")

        return redirect(
            reverse("personalAccount:personal")
        )
    else:
        return redirect(reverse("personalAccount:personal"))
