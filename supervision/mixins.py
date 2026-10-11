from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model

User = get_user_model()

class SupervisorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == User.Role.SUPERVISOR

class SupervisorAccessMixin(LoginRequiredMixin, SupervisorRequiredMixin):
    pass