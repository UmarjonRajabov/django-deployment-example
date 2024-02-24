from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from datetime import datetime

from django.db.models.functions import Now

from back_project import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User


class CustomUser(AbstractUser):
    name = models.CharField(max_length=30)
    username = models.CharField(unique=True, max_length=30)
    table_number = models.CharField(max_length=10, unique=False)
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.name


# Create your models here.

# calc/models.py

class ExcelFile(models.Model):
    file = models.FileField(upload_to='excel_files/')
    uploaded_at = models.DateTimeField(default=datetime.now, blank=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def file_path(self):
        return self.file.path[len(settings.MEDIA_ROOT):]

    def __str__(self):
        return self.file.name


class Employee(models.Model):
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    branch = models.TextField()
    division = models.TextField()
    department = models.TextField()
    table_number = models.CharField(max_length=10, unique=False)
    start = models.DateField(null=True)
    end = models.DateField(null=True)
    photo = models.ImageField(upload_to='employee_photos', blank=True, null=True)

    # user_id = models.FloatField(unique=True)

    # Add other relevant fields

    def __str__(self):
        return f"{self.name} - {self.position}"


class KPI(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.DateField()
    performance_score = models.FloatField()
    kpi_name = models.CharField(max_length=255)
    metric = models.CharField(max_length=255)
    fact = models.FloatField()
    finished = models.FloatField(null=True)
    premium = models.TextField()
    definition = models.TextField()
    method = models.TextField()
    weight = models.FloatField(null=True)
    activity = models.CharField(max_length=4, default='Нет')
    overall = models.FloatField(null=True)

    def __str__(self):
        return self.kpi_name
    # Add other KPI-related fields
