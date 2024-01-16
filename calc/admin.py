from django.contrib import admin
from .models import KPI, Employee


class KPIAdmin(admin.ModelAdmin):
    list_display = ('performance_score', 'kpi_name', 'metric', 'fact')  # Add or modify fields as needed


# Register your models here.
admin.site.register(KPI, KPIAdmin)
admin.site.register(Employee)
