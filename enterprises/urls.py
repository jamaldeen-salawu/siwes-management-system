from django.urls import path
from . import views

app_name = 'enterprises'
urlpatterns = [
    path('<int:pk>/detail/', views.EnterpriseDetailView.as_view(), name='detail'),
    path('create/', views.EnterpriseCreationView.as_view(), name='create'),
    path('', views.EnterpriseList.as_view(), name='list'),
]