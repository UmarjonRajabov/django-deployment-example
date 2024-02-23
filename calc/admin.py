from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import KPI, Employee


class KPIAdmin(admin.ModelAdmin):
    list_display = ('performance_score', 'kpi_name', 'metric', 'fact')  # Add or modify fields as needed


# Register your models here.
admin.site.register(KPI, KPIAdmin)


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'branch', 'division', 'department', 'table_number', 'start', 'end', 'photo')


admin.site.register(Employee, EmployeeAdmin)


class CustomUserAdmin(UserAdmin):
    # Add any customization for the admin view of your custom user model
    pass


admin.site.register(CustomUser, CustomUserAdmin)
