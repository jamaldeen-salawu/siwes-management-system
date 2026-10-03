from django.contrib import admin
from .models import Department, Supervisor, DepartmentStaff
# Register your models here.

admin.site.register(Department)
admin.site.register(Supervisor)
admin.site.register(DepartmentStaff)