from django.shortcuts import render
from django.views import generic
from .models import Student, Placement
from django.shortcuts import reverse, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import (
    UserUpdateForm,
    StudentUpdateForm,
    PlacementForm
)
from django.db import transaction
# Create your views here.
class StudentProfileView(LoginRequiredMixin, generic.DetailView):
    model = Student
    template_name = 'students/student_detail.html'

    def get_object(self):
        return self.request.user.student

def StudentUpdateView(request):
    user = request.user
    student = user.student

    user_form = UserUpdateForm(instance=user)
    student_form = StudentUpdateForm(instance=student)
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        student_form = StudentUpdateForm(request.POST, instance=student)
        if user_form.is_valid() and student_form.is_valid():
            with transaction.atomic():
                user_form.save()
                student_form.save()
                return redirect('students:profile')
    context = {
        'user_form': user_form,
        'student_form': student_form
    }
    return render(request, 'students/student_update.html', context)

class StudentPlacementView(generic.DetailView):
    template_name = 'students/placement_detail.html'
    model = Placement
    def get_object(self):
        return self.request.user.student.placement

class StudentPlacementCreateView(generic.CreateView):
    form_class = PlacementForm
    template_name = 'students/placement_form.html'
    def get_success_url(self):
        return reverse('students:placement')

    def form_valid(self, form):
        placement = form.save(commit=False)
        placement.student = self.request.user.student
        placement.save()
        return super().form_valid(form)

class StudentUpdatePlacementView(generic.UpdateView):
    template_name = 'students/placement_form.html'
    form_class = PlacementForm

    def get_object(self):
        return self.request.user.student.placement

    def get_success_url(self):
        return reverse('students:placement')

class StudentAssignedSupervisorView(generic.DetailView):
    model = Student
    template_name = 'students/student_supervisor.html'

    def get_object(self):
        return self.request.user.student

class StudentSupervisionVisitView(generic.DetailView):
    model = Student
    template_name = 'students/supervision_visit.html'

    def get_object(self):
        return self.request.user.student
