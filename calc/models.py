from django.db import models


# Create your models here.

# calc/models.py

class Employee(models.Model):
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    # Add other relevant fields


class KPI(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.DateField()
    performance_score = models.FloatField()
    kpi_name = models.CharField(max_length=255, default='default_value')
    metric = models.CharField(max_length=255, default='default_value')
    fact = models.FloatField()
    finished = models.FloatField(null=True)
    premium = models.FloatField(null=True)
    definition = models.TextField(default='default_value')
    method = models.TextField(default='default_value')
    weight = models.FloatField(null=True)
    activity = models.CharField(max_length=4, default='Нет')
    overall = models.FloatField(null=True)

    def __str__(self):
        return self.kpi_name
    # Add other KPI-related fields
