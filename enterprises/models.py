from django.db import models
from students.constants import NIGERIAN_LOCATIONS
from departments.models import Department
# Create your models here.
STATE_CHOICES = [(location, location.upper()) for location in NIGERIAN_LOCATIONS]

class Enterprise(models.Model):
    name = models.CharField(max_length=20)
    branch = models.CharField(max_length=100, blank=True)
    address = models.TextField()
    state = models.CharField(max_length=11, choices=STATE_CHOICES)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='enterprises')

    def __str__(self):
        return self.name

