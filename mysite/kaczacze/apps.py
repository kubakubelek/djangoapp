from django.apps import AppConfig


class KaczaczeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = 'mysite.kaczacze'


    def ready(self):
        pass
