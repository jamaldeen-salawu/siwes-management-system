from django import forms
from .models import Department
from students.models import Student
from supervision.models import Supervisor

class AssignSupervisorForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'supervisor'
        ]

