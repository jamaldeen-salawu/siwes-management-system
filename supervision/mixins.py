from students.models import Student

class SupervisorAuthorizationMixin:
    def get_queryset(self):
        return Student.objects.filter(supervisor=self.request.user.supervisor)