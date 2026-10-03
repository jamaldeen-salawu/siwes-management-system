from django.db import models
from students.constants import NIGERIAN_LOCATIONS
# Create your models here.
STATE_CHOICES = [(location, location.upper()) for location in NIGERIAN_LOCATIONS]

class Enterprise(models.Model):
    name = models.CharField(max_length=20)
    address = models.TextField()
    state = models.CharField(max_length=11, choices=STATE_CHOICES)

    def __str__(self):
        return self.name

