from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth import get_user_model

User = get_user_model()


class StudentRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == User.Role.STUDENT

class StudentAccessMixin(LoginRequiredMixin, StudentRequiredMixin):
    pass
