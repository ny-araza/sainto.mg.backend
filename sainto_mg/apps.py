from django.apps import AppConfig


class SaintoMgConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "sainto_mg"

    def ready(self):
        import sainto_mg.signals  # noqa
