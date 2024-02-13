from django.apps import AppConfig
from django.contrib.auth import get_user_model


class CalcConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'calc'

    def ready(self):

        import calc.signals  # This imports the signals module when the app is ready
