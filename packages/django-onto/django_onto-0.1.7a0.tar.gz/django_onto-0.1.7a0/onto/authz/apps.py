from django.apps import AppConfig


class ontoAuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'onto.authz'
    label = 'onto_authz'

    def ready(self) -> None:
        super().ready()
        from . import signals