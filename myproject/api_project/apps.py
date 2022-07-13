from django.apps import AppConfig


class ApiProjectConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api_project'

    def ready(self):
        from .signals import create_profile, save_profile