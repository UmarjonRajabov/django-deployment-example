# Generated by Django 5.0.1 on 2024-01-30 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0009_alter_kpi_premium'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kpi',
            name='month',
            field=models.DateTimeField(),
        ),
    ]
