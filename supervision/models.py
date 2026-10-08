from django.db import models
from django.conf import settings
from departments.models import Department


class Supervisor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='supervisors')
    phone_no = models.CharField(max_length=11)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

