from django.db import models
from django.conf import settings
from supervision.models import Department, Supervisor
from .constants import NIGERIAN_LOCATIONS, LEVEL
from enterprises.models import Enterprise
# Create your models here.


LEVELS = [(level[:3], level.upper()) for level in LEVEL]

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='students')
    supervisor = models.ForeignKey(Supervisor, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    phone_no = models.CharField(max_length=11)
    matric_no = models.CharField(max_length=20)
    level = models.CharField(max_length=3, choices=LEVELS)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Placement(models.Model):
    class Status(models.TextChoices):
        VISITED = "VISITED", "Visited"
        NOT_VISITED = "NOT_VISITED", "Not visited"
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, related_name='placements')

    session = models.CharField(max_length=9)


    on_site_days = models.JSONField(default=list)
    resumption_time = models.TimeField()
    closing_time = models.TimeField()

    start_date = models.DateField()
    end_date = models.DateField()

    visit_status = models.CharField(max_length=20, choices=Status.choices, default=Status.NOT_VISITED)
    planned_date = models.DateField(null=True, blank=True)
    visit_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.enterprise.name
