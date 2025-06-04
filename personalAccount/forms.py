from django import forms
from .models import DeliveryProfile

class DeliveryProfileForm(forms.ModelForm):
    class Meta:
        model = DeliveryProfile
        fields = ['city', 'street', 'house', 'entrance', 'floor', 'needs_elevator', 'has_lift'] # Добавлено has_lift
        widgets = {
            'floor': forms.NumberInput(attrs={'min': 1}),
        }