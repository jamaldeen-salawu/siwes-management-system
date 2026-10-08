from django.urls import path
from . import views

app_name = 'departments'

urlpatterns = [
    # dashboard
    path('dashboard/', views.StaffDashboardView.as_view(), name='dashboard'),
    # department
    path('department-view/', views.StaffDepartmentView.as_view(), name='department-view'),
    path('department-create/', views.DepartmentCreateView.as_view(), name='department-create'),
    path('department-update/', views.DepartmentUpdateView.as_view(), name='department-update'),
    # students
    path('student/list/', views.StaffStudentListView.as_view(), name='student-list'),
    path('student/<int:pk>/detail/', views.StaffStudentDetailView.as_view(), name='student-detail'),
    path('student/create/', views.StaffStudentCreateView, name='student-create'),
    path('student/<int:pk>/update/', views.StaffStudentUpdateView, name='student-update'),
    path('student/<int:pk>/assign-supervisor/', views.AssignSupervisor.as_view(), name='assign-supervisor'),
    # supervisor
    path('supervisor/list/', views.StaffSupervisorListView.as_view(), name='supervisor-list'),
    path('supervisor/<int:pk>/detail/', views.StaffSupervisorDetailsView.as_view(), name='supervisor-detail'),
    path('supervisor/create/', views.StaffSupervisorCreateView, name='supervisor-create'),
    path('supervisor/<int:pk>/update/', views.StaffSupervisorUpdateView, name='supervisor-update'),
    # staff
    path('staff/list/', views.StaffDepartmentStaffListView.as_view(), name='staff-list'),
    path('staff/<int:pk>/detail/', views.StaffDepartmentStaffDetailsView.as_view(), name='staff-detail'),
    path('staff/create/', views.StaffDepartmentStaffCreateView, name='staff-create'),
    path('staff/<int:pk>/update/', views.StaffDepartmentStaffUpdateView, name='staff-update'),
    # placement
    path('placements/', views.PlacementListView.as_view(), name='placement-list'),
    path('student/<int:pk>/placement/create/', views.StaffStudentPlacementCreateView.as_view(), name='placement-create'),
    path('student/<int:pk>/placement/update/', views.StaffStudentPlacementUpdateView.as_view(), name='placement-update'),
    # enterprise
    path('enterprises/', views.StaffEnterpriseListView.as_view(), name='enterprise-list'),
    path('enterprises/create/', views.StaffEnterpriseCreateView.as_view(), name='enterprise-create'),
    path('enterprises/<int:pk>/update/', views.StaffEnterpriseUpdateView.as_view(), name='enterprise-update'),
    path('enterprises/<int:pk>/detail/', views.StaffEnterpriseDetailView.as_view(), name='enterprise-detail'),
    # supervision
    path('supervision/', views.StaffSupervisionListView.as_view(), name='supervision')
]