from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Employee


# Create or update Employee instances upon user creation/update
@receiver(post_save, sender=get_user_model())
def create_or_update_employee(sender, instance, created, **kwargs):
    if created:
        Employee.objects.create(user=instance)
    else:
        if hasattr(instance,'employee'):
            instance.employee.save()
