from django.shortcuts import render, reverse
from django.views import generic
from django.db import transaction
from .forms import (
    RoleSelection,
    GenericUserForm, 
    StudentSignupForm,
    SupervisorSignupForm,
    StaffSignupForm,
)
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView 
# Create your views here.
User = get_user_model()

class RoleSelection(generic.FormView):
    form_class = RoleSelection
    template_name = 'accounts/role-select.html'
    def form_valid(self, form):
        role = form.cleaned_data['role']
        if role == User.Role.STUDENT:
            return redirect('accounts:student-signup')
        if role == User.Role.SUPERVISOR:
            return redirect('accounts:supervisor-signup')
        if role == User.Role.STAFF:
            return redirect('accounts:department-signup')


def StudentSignup(request):
    user_form = GenericUserForm()
    student_form = StudentSignupForm()
    if request.method == 'POST':
        user_form = GenericUserForm(request.POST)
        student_form = StudentSignupForm(request.POST)
        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save(commit=False)
            user.role = User.Role.STUDENT
            student = student_form.save(commit=False)
            student.user = user
            with transaction.atomic():
                user.save()
                student.save()
            return redirect('accounts:login')
    context = {
        'user_form': user_form,
        'student_form': student_form
    }
    return render(request, 'accounts/student-signup.html', context)

def SupervisorSignup(request):
    user_form = GenericUserForm()
    supervisor_form = SupervisorSignupForm()
    if request.method == 'POST':
        user_form = GenericUserForm(request.POST)
        supervisor_form = SupervisorSignupForm(request.POST)
        if user_form.is_valid() and supervisor_form.is_valid():
            user = user_form.save(commit=False)
            user.role = User.Role.SUPERVISOR
            supervisor = supervisor_form.save(commit=False)
            supervisor.user = user
            with transaction.atomic():
                user.save()
                supervisor.save()
            return redirect('accounts:login')
    context = {
        'user_form': user_form,
        'supervisor_form': supervisor_form
    }
    return render(request, 'accounts/supervisor-signup.html', context)

def DepartmentSignup(request):
    user_form = GenericUserForm()
    staff_form = StaffSignupForm()
    if request.method == 'POST':
        user_form = GenericUserForm(request.POST)
        staff_form = StaffSignupForm(request.POST)
        if user_form.is_valid() and staff_form.is_valid():
            user = user_form.save(commit=False)
            user.role = User.Role.STAFF
            staff = staff_form.save(commit=False)
            staff.user = user
            with transaction.atomic():
                user.save()
                staff.save()
            return redirect('accounts:login')
    context = {
        'user_form': user_form,
        'staff_form': staff_form
    }
    return render(request, 'accounts/staff-signup.html', context)


class CustomLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user
        if user.role == 'STUDENT':
            return reverse('students:placement')
        if user.role == 'SUPERVISOR':
            return reverse('supervision:students')
