from django.db import models
from django.conf import settings

# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)

    def __str__(self):
        return self.code


class DepartmentStaff(models.Model):
    class Title(models.TextChoices):
        HOD = "HOD", "Head of Department"
        ADMIN = "ADMIN", "Department Admin"
        SIWES_COORDINATOR = "SIWES_COORDINATOR", "SIWES Coordinator"

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='staffs', null=True, blank=True)
    title = models.CharField(max_length=20, choices=Title.choices)
