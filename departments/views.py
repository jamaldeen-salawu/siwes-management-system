from django.shortcuts import render, reverse, get_object_or_404
from django.views import generic
from .models import DepartmentStaff
from students.models import Student, Placement
from supervision.models import Supervisor
from .models import Department, DepartmentStaff
from accounts.forms import DepartmentForm, GenericUserForm, StudentSignupForm, SupervisorSignupForm, StaffSignupForm
from django.db import transaction
from .forms import AssignSupervisorForm
from django.db.models import Count
from students.forms import PlacementForm
from enterprises.forms import EnterpriseForm
from enterprises.models import Enterprise
# Create your views here.

#-----------DASHBOARD-------------

class StaffDashboardView(generic.TemplateView):
    template_name = 'departments/dashboards.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        students = Student.objects.filter(department=self.request.user.departmentstaff.department).count()
        supervisors = Supervisor.objects.filter(department=self.request.user.departmentstaff.department).count()
        student_placement = Student.objects.filter(department=self.request.user.departmentstaff.department, placement_isnull=False).count()
        upcoming_visit = Placement.objects.filter(
            student__department=self.request.user.departmentstaff.department
        ).filter(
            visit_status=Placement.Status.NOT_VISITED
            ).order_by('planned_date')
        visited = Placement.objects.filter(
            student__supervisor=self.request.user.departmentstaff.department
            ).filter(visit_status=Placement.Status.VISITED).count()
        not_visited = Placement.objects.filter(
            student__supervisor=self.request.user.departmentstaff.department
            ).filter(visit_status=Placement.Status.NOT_VISITED).count() 
        context.update({
            'students': students,
            'supervisors': supervisors,
            'student_placement': student_placement,
            'upcoming_visits': upcoming_visit,
            'visited': visited,
            'not_visited': not_visited
           })
        return context

#---------------DEPARTMENT------------------
        
class StaffDepartmentView(generic.DetailView):
    model = Department
    template_name = 'departments/department_view.html'

    def get_object(self):
        return self.request.user.departmentstaff.department

class DepartmentUpdateView(generic.UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'departments/department_update.html'

    def get_object(self):
        return self.request.user.departmentstaff.department

    def get_success_url(self):
        return reverse('departments:department-view')

class DepartmentCreateView(generic.CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'departments/department_create.html'

    def get_success_url(self):
        return reverse('departments:department-view')

#------------------STUDENT------------------
class StaffStudentListView(generic.ListView):
    model = Student
    template_name = 'departments/student_list.html'
    context_object_name = 'students'

    def get_queryset(self):
        return Student.objects.filter(department=self.request.user.departmentstaff.department)

class StaffStudentDetailView(generic.DetailView):
    model = Student
    template_name = 'departments/student_detail.html'
    
    def get_queryset(self):
        return Student.objects.filter(department=self.request.user.departmentstaff.department)

def StaffStudentCreateView(request):
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

            return redirect('departments:student-detail', pk=student.id)
    context = {
        'user_form': user_form,
        'student_form': student_form
    }
    return render(request, 'departments/student_create.html', context)

def StaffStudentUpdateView(request, pk):
    student = get_object_or_404(Student.objects.filter(department=request.user.departmentstaff.department), id=pk)
    user = student.user

    user_form = GenericUserForm(instance=user)
    student_form = StudentSignupForm(instance=student)
    if request.method == 'POST':
        user_form = GenericUserForm(request.POST, instance=user)
        student_form = StudentSignupForm(request.POST, instance=student)
        if user_form.is_valid() and student_form.is_valid():
            with transaction.atomic():
                user_form.save()
                student_form.save()  
                return redirect('departments:student-detail', pk=student.id)      
    context = {
        'user_form': user_form,
        'student_form': student_form
    }
    return render(request, 'departments/student_update.html', context)

class AssignSupervisor(generic.UpdateView):
    form_class = AssignSupervisorForm
    template_name = 'departments/assign_supervisor.html'

    def get_queryset(self):
        return Student.objects.filter(department=self.request.user.departmentstaff.department)

    def get_success_url(self):
        return reverse('departments:student-detail', args=(student.id,))

#-------------------SUPERVISOR-----------------------------

class StaffSupervisorListView(generic.ListView):
    model = Supervisor
    template_name = 'departments/supervisor_list.html'
    context_object_name = 'supervisors'

    def get_queryset(self):
        return Supervisor.objects.filter(
            department=self.request.user.departmentstaff.department
        ).annotate(
            student_count=Count('students')
        )

class StaffSupervisorDetailsView(generic.DetailView):
    model = Supervisor
    template_name = 'departments/supervisor_detail.html'

    def get_queryset(self):
        return Supervisor.objects.filter(
            department=self.request.user.departmentstaff.department
        ).annotate(
            student_count=Count('students')
        )
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        students = Student.objects.filter(supervisor=self.object)
        context['students'] = students
        return context

def StaffSupervisorCreateView(request):
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
            return redirect('departments:supervisor-detail', pk=supervisor.id)

    context = {
        'user_form': user_form,
        'supervisor_form': supervisor_form
    }
    return render(request, 'departments/supervisor_create.html', context)


def StaffSupervisorUpdateView(request, pk):
    supervisor = get_object_or_404(Supervisor.objects.filter(department=request.user.departmentstaff.department), id=pk)
    user = supervisor.user

    user_form = GenericUserForm(instance=user)
    supervisor_form = SupervisorSignupForm(instance=supervisor)
    if request.method == 'POST':
        user_form = GenericUserForm(request.POST, instance=user)
        supervisor_form = SupervisorSignupForm(request.POST, instance=supervisor)
        if user_form.is_valid() and supervisor_form.is_valid():
            with transaction.atomic():
                user_form.save()
                supervisor_form.save()  
                return redirect('departments:supervisor-detail', pk=supervisor.id)      
    context = {
        'user_form': user_form,
        'supervisor_form': supervisor_form
    }
    return render(request, 'departments/supervisor_update.html', context)


#-------------------------------Staff-----------------------------

class StaffDepartmentStaffListView(generic.ListView):
    model = DepartmentStaff
    template_name = 'departments/staff_list.html'

    def get_queryset(self):
        return DepartmentStaff.objects.filter(
            department=self.request.user.departmentstaff.department
        )

class StaffDepartmentStaffDetailsView(generic.DetailView):
    model = DepartmentStaff
    template_name = 'departments/staff_detail.html'

    def get_queryset(self):
        return DepartmentStaff.objects.filter(
            department=self.request.user.departmentstaff.department
        )

def StaffDepartmentStaffCreateView(request):
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
            return redirect('departments:staff-detail', pk=staff.id)

    context = {
        'user_form': user_form,
        'staff_form': staff_form
    }
    return render(request, 'departments/staff_create.html', context)


def StaffDepartmentStaffUpdateView(request, pk):
    staff = get_object_or_404(DepartmentStaff.objects.filter(department=request.user.departmentstaff.department), id=pk)
    user = staff.user

    user_form = GenericUserForm(instance=user)
    staff_form = StaffSignupForm(instance=staff)
    if request.method == 'POST':
        user_form = GenericUserForm(request.POST, instance=user)
        staff_form = StaffSignupForm(request.POST, instance=staff)
        if user_form.is_valid() and staff_form.is_valid():
            with transaction.atomic():
                user_form.save()
                staff_form.save()  
            return redirect('departments:staff-detail', pk=staff.id)      
    context = {
        'user_form': user_form,
        'staff_form': staff_form
    }
    return render(request, 'departments/staff_update.html', context)

#---------------PLACEMENT-------------------

class PlacementListView(generic.ListView):
    model = Student
    template_name = 'departments/placement_list.html'

    def get_queryset(self):
        return Student.objects.filter(department=self.request.user.departmentstaff.department, placement__isnull=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['no_placement'] = Student.objects.filter(
            department=self.request.user.departmentstaff.department,
            placement__isnull=True
        )
        return context

class StaffStudentPlacementCreateView(generic.CreateView):
    form_class = PlacementForm
    template_name = 'departments/placement_create.html'

    def form_valid(self, form):
        placement = form.save(commit=False)
        student = get_object_or_404(
            Student.objects.filter(department=self.request.user.departmentstaff.department),
            id=self.kwargs['pk']
            )
        placement.student = student
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('departments:student-detail', args=(self.kwargs['pk'],))

class StaffStudentPlacementUpdateView(generic.UpdateView):
    form_class = PlacementForm
    template_name = 'departments/placement_update.html'

    def get_object(self):
        student = get_object_or_404(
            Student.objects.filter(department=self.request.user.departmentstaff.department),
            id=self.kwargs['pk']
        )
        placement = get_object_or_404(Placement, student=student)
        return placement

        def get_success_url(self):
            return reverse('departments:student-detail', args=(self.kwargs['pk'],))

#-------------------------ENTERPRISE---------------------------

class StaffEnterpriseListView(generic.ListView):
    model = Enterprise
    template_name = 'departments/enterprise_list.html'

    def get_queryset(self):
        return Enterprise.objects.filter(department=self.request.user.departmentstaff.department)

class StaffEnterpriseCreateView(generic.CreateView):
    form_class = EnterpriseForm
    template_name = 'departments/enterprise_form.html'

    def get_success_url(self):
        return reverse('departments:enterprise-detail', args=(self.object.id,))

    def form_valid(self, form):
        form.instance.department = self.request.user.departmentstaff.department
        return super().form_valid(form)
 
class StaffEnterpriseUpdateView(generic.UpdateView):
    form_class = EnterpriseForm
    template_name = 'departments/enterprise_form.html'

    def get_success_url(self):
        return reverse('departments:enterprise-detail', args=(self.object.id,))
    
    def get_queryset(self):
        return Enterprise.objects.filter(department=self.request.user.departmentstaff.department)


class StaffEnterpriseDetailView(generic.DetailView):
    model = Enterprise
    template_name = 'departments/enterprise_detail.html'

    def get_queryset(self):
        return Enterprise.objects.filter(department=self.request.user.departmentstaff.department)

#----------------------SUPERVISION VISITS------------------------

class StaffSupervisionListView(generic.ListView):
    model = Placement
    template_name = 'departments/supervision.html'
    context_object_name = 'upcoming_visits'

    def get_queryset(self):
        return Placement.objects.filter(
            student__department=self.request.user.departmentstaff.department,
            visit_status=Placement.Status.NOT_VISITED
            ).order_by('planned_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        visited = Placement.objects.filter(
            student__department=self.request.user.departmentstaff.department,
            visit_status=Placement.Status.VISITED
        ).order_by('visit_date')
        context['visited'] = visited
        return context