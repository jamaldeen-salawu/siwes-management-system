from django import forms
from students.models import Placement
from .models import Supervisor
from django.contrib.auth import get_user_model


User = get_user_model()

class UpdateSupervisionForm(forms.ModelForm):
    """
    Update supervision status form
    """
    class Meta:
        model = Placement
        fields = [
            'visit_status',
            'planned_date',
            'visit_date'
        ]
        widgets = {
            'planned_date': forms.DateInput(attrs={'type': "date"}),
            'visit_date': forms.DateInput(attrs={'type': "date"})
        }

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
        ]
class SupervisorUpdateForm(forms.ModelForm):
    class Meta:
        model = Supervisor
        fields = [
            'department',
            'phone_no',
        ]