from django import forms
from .models import Student, Placement
from django.contrib.auth import get_user_model
from .constants import DAYS
from enterprises.models import Enterprise

User = get_user_model()

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
        ]
class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'matric_no',
            'phone_no',
            'department',
            'level'
        ]

class PlacementForm(forms.ModelForm):
    on_site_days = forms.MultipleChoiceField(choices=DAYS, widget=forms.CheckboxSelectMultiple)
    def __init__(self, *args, **kwargs):
        student = kwargs.pop('student')
        super().__init__(*args, **kwargs)
        self.fields['enterprise'].queryset = Enterprise.objects.filter(
            department=student.department
        )
    class Meta:
        model = Placement
        fields = [
            'enterprise',
            'session',
            'start_date',
            'end_date',
            'on_site_days',
            'resumption_time',
            'closing_time'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'resumption_time': forms.TimeInput(attrs={'type': 'time'}),
            'closing_time': forms.TimeInput(attrs={'type': 'time'}),
        }
