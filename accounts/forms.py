from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from students.models import Student
from supervision.models import Supervisor
from departments.models import Department, DepartmentStaff

User = get_user_model()

class RoleSelection(forms.Form):
    role = forms.ChoiceField(choices=User.Role.choices)

class GenericUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
        ]

class StudentSignupForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'department',
            'matric_no',
            'level',
            'phone_no',
        ]

class SupervisorSignupForm(forms.ModelForm):
    class Meta:
        model = Supervisor
        fields = [
            'phone_no',
            'department'
        ]

class StaffSignupForm(forms.ModelForm):
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=False
    )
    class Meta:
        model = DepartmentStaff
        fields = [
            'department',
            'title'
        ]

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = [
            'name',
            'code'
        ]