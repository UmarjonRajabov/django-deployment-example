# Generated by Django 5.0.1 on 2024-04-04 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kpi',
            name='month',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='kpiarchive',
            name='month',
            field=models.DateField(),
        ),
    ]
