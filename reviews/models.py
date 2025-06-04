from django.db import models
from django.contrib.auth.models import User


class Review(models.Model):
    text = models.TextField(verbose_name="Текст отзыва")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Автор", default=1
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_published = models.BooleanField(default=False, verbose_name="Опубликовано")
    rating = models.IntegerField(
        default=5, verbose_name="Рейтинг", choices=[(i, i) for i in range(1, 6)]
    )

    def __str__(self):
        return f"Отзыв от {self.author.username} ({self.created_at})"

    class Meta:
        db_table = "review"
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
