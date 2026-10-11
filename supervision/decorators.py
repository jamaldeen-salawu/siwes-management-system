from functools import wraps
from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model

User = get_user_model()

def supervisor_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.role != User.Role.SUPERVISOR:
            raise PermissionDenied

        return view_func(request, *args, **kwargs)
    
    return wrapper