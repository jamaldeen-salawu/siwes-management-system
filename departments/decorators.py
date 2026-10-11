from functools import wraps
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model

User = get_user_model()

def department_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.departmentstaff.department is None:
            return redirect('departments:department-create')

        return view_func(request, *args, **kwargs)

    return wrapper

def staff_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.role != User.Role.STAFF:
            raise PermissionDenied

        return view_func(request, *args, **kwargs)

    return wrapper 