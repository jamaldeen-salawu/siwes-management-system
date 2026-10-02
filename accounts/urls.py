from django.urls import path
from . import views 
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

app_name = 'accounts'
urlpatterns = [
    path("signup/", views.RoleSelection.as_view(), name='signup'),
    path("signup/student/", views.StudentSignup, name='student-signup'),
    path("signup/supervisor/", views.SupervisorSignup, name='supervisor-signup'),
    path("signup/department/", views.DepartmentSignup, name='department-signup'),
    path("login/", LoginView.as_view(), name='login'),
    path("logout/", LogoutView.as_view(), name='logout'),
    path("password-reset/", PasswordResetView.as_view(), name='password-reset'),
    path("password-reset-done/", PasswordResetDoneView.as_view(), name='password-reset-done'),
    path("password-reset-confirm/<uidb64>/<token>/", PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path("password-reset-complete/", PasswordResetCompleteView.as_view(), name='password-reset-complete'),
]