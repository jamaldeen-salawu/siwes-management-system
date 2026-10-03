from django import forms
from .models import Enterprise
from django.contrib.auth import get_user_model

User = get_user_model()

class EnterpriseCreationForm(forms.ModelForm):
    class Meta:
        model = Enterprise
        fields = [
            'name',
            'state',
            'address',
        ]