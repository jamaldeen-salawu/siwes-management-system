from django.urls import path
from . import views

app_name = 'students'
urlpatterns = [
    path('profile/', views.StudentProfileView.as_view(), name='profile'),
    path('update/', views.StudentUpdateView, name='update'),
    path('placement/create/', views.StudentPlacementCreateView.as_view(), name='placement-create'),
    path('placement/detail/', views.StudentPlacementView.as_view(), name='placement'),
    path('supervisor/', views.StudentAssignedSupervisorView.as_view(), name='assigned-supervisor'),
    path('supervision-visit/', views.StudentSupervisionVisitView.as_view(), name='supervision-visit'),
    path('placement/update/', views.StudentUpdatePlacementView.as_view(), name='placement-update'),
]