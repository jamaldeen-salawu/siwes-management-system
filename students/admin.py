from django.contrib import admin
from .models import Student, Placement, Enterprise
# Register your models here.
admin.site.register(Student)
admin.site.register(Placement)
admin.site.register(Enterprise)