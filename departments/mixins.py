from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect

class DepartmentRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.departmentstaff.department is None:
            return redirect('departments:department-create')
        return super().dispatch(request, *args, **kwargs)