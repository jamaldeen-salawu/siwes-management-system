from django.urls import path
from . import views

app_name = 'supervision'

urlpatterns = [
    path('my-students/', views.SupervisorAssignedStudentsView.as_view(), name='students'),
    path('<int:pk>/', views.StudentDetailView.as_view(), name='student-detail'),
    path('<int:pk>/update/', views.UpdateSupervisionStatusView.as_view(), name='update-supervision-status'),
]