# Generated by Django 5.0.1 on 2024-01-16 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0006_kpi_activity'),
    ]

    operations = [
        migrations.AddField(
            model_name='kpi',
            name='overall',
            field=models.FloatField(null=True),
        ),
    ]
