from django.urls import path
from . import views

app_name = 'supervision'

urlpatterns = [
    path('my-students/', views.SupervisorAssignedStudentsView.as_view(), name='students'),
    path('profile/', views.SupervisorProfileView.as_view(), name='profile'),
    path('profile/update/', views.SupervisorUpdateProfileView, name='update-profile'),
    path('upcoming-visits/', views.UpcomingVisitView.as_view(), name='upcoming'),
    path('enterprise-list/', views.SupervisorEnterpriseListView.as_view(), name='enterprise-list'),
    path('<int:pk>/enterprise-detail/', views.SupervisorEnterpriseDetailView.as_view(), name='enterprise-detail'),
    path('<int:pk>/', views.StudentDetailView.as_view(), name='student-detail'),
    path('<int:pk>/placement/detail/', views.PlacementDetailView.as_view(), name='placement-detail'),
    path('<int:pk>/update/', views.UpdateSupervisionStatusView.as_view(), name='update-supervision-status'),
]