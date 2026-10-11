from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib.auth import get_user_model

User = get_user_model()

class DepartmentRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.departmentstaff.department is None:
            return redirect('departments:department-create')
        return super().dispatch(request, *args, **kwargs)


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.role == User.Role.STAFF:
            return True
        return False

class DepartmentStaffCheckMixin(
    LoginRequiredMixin,
    StaffRequiredMixin,
    DepartmentRequiredMixin
):
    pass

class CreateDepartmentOnceMixin(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.departmentstaff.department:
            return redirect('departments:dashboard')

class CreateDepartmentOnceMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.departmentstaff.department:
            return redirect('departments:dashboard')
        return super().dispatch(request, *args, **kwargs)