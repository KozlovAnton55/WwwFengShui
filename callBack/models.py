from django.db import models

class CallBackRequest(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  
    viewed = models.BooleanField(default=False) 

    def __str__(self):
        return f"{self.name} - {self.phone}"

    class Meta:
        verbose_name = "Заявку"
        verbose_name_plural = "Заявки от пользователей сайтом на обратный звонок"
        ordering = ['-created_at']  
