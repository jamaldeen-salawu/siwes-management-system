from django.shortcuts import render, reverse, redirect
from django.views import generic
from students.models import Student, Placement
from enterprises.models import Enterprise
from .mixins import SupervisorAuthorizationMixin
from .forms import UpdateSupervisionForm, SupervisorUpdateForm, UserUpdateForm
from .models import Supervisor
from students.forms import UserUpdateForm
from django.db import transaction
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

class UpcomingVisitView(generic.ListView):
    model = Placement
    template_name = 'supervision/upcoming_visits.html'
    context_object_name = 'placements'

    def get_queryset(self):
        queryset = Placement.objects.filter(student__supervisor=self.request.user.supervisor)
        queryset = queryset.filter(visit_status=Placement.Status.NOT_VISITED).order_by("planned_date")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = Placement.objects.filter(
            student__supervisor=self.request.user.supervisor
            ).filter(visit_status=Placement.Status.VISITED).order_by('visit_date')
        context['visited'] = queryset
        return context

class PlacementDetailView(generic.DetailView):
    model = Placement
    template_name = 'supervision/placement_detail.html'

    def get_queryset(self):
        return Placement.objects.filter(student__supervisor=self.request.user.supervisor)

class SupervisorProfileView(generic.DetailView):
    model = Supervisor
    template_name = 'supervision/supervisor_profile.html'

    def get_object(self):
        return self.request.user.supervisor

def SupervisorUpdateProfileView(request):
    user = request.user
    supervisor = user.supervisor

    user_form = UserUpdateForm(instance=user)
    supervisor_form = SupervisorUpdateForm(instance=supervisor)
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        supervisor_form = SupervisorUpdateForm(request.POST, instance=supervisor)       
        if user_form.is_valid() and supervisor_form.is_valid():
            with transaction.atomic():
                user_form.save()
                supervisor_form.save()
                return redirect('supervision:profile')
    context = {
        'user_form': user_form,
        'supervisor_form': supervisor_form
    }
    return render(request, 'supervision/supervisor_update.html', context)

class SupervisorEnterpriseListView(generic.ListView):
    model = Enterprise
    context_object_name = "enterprises"
    template_name = 'supervision/enterprise_list.html'

    def get_queryset(self):
        return Enterprise.objects.filter(
            placements__student__supervisor=self.request.user.supervisor
        ).distinct()

class SupervisorEnterpriseDetailView(generic.DetailView):
    model = Enterprise
    template_name = 'supervision/enterprise_detail.html'

    def get_queryset(self):
        return Enterprise.objects.filter(
            placements__student__supervisor=self.request.user.supervisor
        ).distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        placements = Placement.objects.filter(
            enterprise=self.object
        ).filter(student__supervisor=self.request.user.supervisor)
        context['placements'] = placements
        return context
