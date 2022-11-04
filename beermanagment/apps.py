from django.apps import AppConfig


class BeermanagmentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'beermanagment'

    def ready(self):
        import beermanagment.signals  # noqa 