from django.urls import path
from . import views

app_name = 'supervision'

urlpatterns = [
    path('my-students/', views.SupervisorAssignedStudentsView.as_view(), name='students'),
    path('profile/', views.SupervisorProfileView.as_view(), name='profile'),
    path('profile/update/', views.SupervisorUpdateProfileView, name='update-profile'),
    path('upcoming-visits/', views.UpcomingVisitView.as_view(), name='upcoming'),
    path('<int:pk>/', views.StudentDetailView.as_view(), name='student-detail'),
    path('<int:pk>/placement/detail/', views.PlacementDetailView.as_view(), name='placement-detail'),
    path('<int:pk>/update/', views.UpdateSupervisionStatusView.as_view(), name='update-supervision-status'),
]