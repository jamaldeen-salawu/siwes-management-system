from django.urls import path
from . import views

app_name = 'students'
urlpatterns = [
    path('profile/', views.StudentProfileView.as_view(), name='profile'),
    path('update/', views.StudentUpdateView, name='placement-update'),
    path('placement/create/', views.StudentPlacementCreateView.as_view(), name='placement-create'),
    path('supervisor/', views.StudentAssignedSupervisorView.as_view(), name='assigned-supervisor'),
    path('supervision-visit/', views.StudentSupervisionVisitView.as_view(), name='supervision-visit'),
    path('placement/update/', views.StudentUpdatePlacementView.as_view(), name='placement-update'),
    # enterprise
    path('enterprises/create/', views.StudentEnterpriseCreateView.as_view(), name='enterprise-create'),
    path('enterprises/<int:pk>/update/', views.StudentEnterpriseUpdateView.as_view(), name='enterprise-update'),
    path('enterprises/<int:pk>/detail/', views.StudentEnterpriseDetailView.as_view(), name='enterprise-detail'),
]