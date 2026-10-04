from django.shortcuts import render, reverse
from django.views import generic
from students.models import Student, Placement
from .mixins import SupervisorAuthorizationMixin
from .forms import UpdateSupervisionForm 
# Create your views here.

class SupervisorAssignedStudentsView(generic.ListView):
    """
    List of students assigned to him
    """
    model = Student
    template_name = 'supervision/Assigned_students.html'
    context_object_name = 'students'

    def get_queryset(self):
        return Student.objects.filter(supervisor=self.request.user.supervisor)

class StudentDetailView(SupervisorAuthorizationMixin, generic.DetailView):
    """
    Supervisor view of details for students assigned to
    """
    model = Student
    template_name = 'supervision/student_detail.html'

class UpdateSupervisionStatusView(generic.UpdateView):
    """
    Update supervision status for individual students
    """
    template_name = 'supervision/update_supervision_status.html'
    form_class = UpdateSupervisionForm

    def get_queryset(self):
        return Placement.objects.filter(student__supervisor=self.request.user.supervisor)
    

    def get_success_url(self):
        return reverse('supervision:student-detail', kwargs={'pk': self.object.student.id})