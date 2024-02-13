from django.apps import AppConfig
from django.contrib.auth import get_user_model


class CalcConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'calc'

    def ready(self):

        from .models import Employee
        # Create or update Employee instances upon user creation/update
        def create_or_update_employee(sender, instance, created, **kwargs):
            if created:
                Employee.objects.create(user=instance)
            else:
                instance.employee.save()

        # Connect signal to user model
        User = get_user_model()
        User.post_save.connect(create_or_update_employee, sender=User)
