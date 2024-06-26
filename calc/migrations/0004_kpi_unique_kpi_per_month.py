# Generated by Django 5.0.1 on 2024-04-07 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0003_alter_kpiarchive_month'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='kpi',
            constraint=models.UniqueConstraint(fields=('user', 'employee', 'month', 'kpi_name'), name='unique_kpi_per_month'),
        ),
    ]
