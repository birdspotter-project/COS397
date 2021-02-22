from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'birdspotter.accounts'
    def ready(self):
        from .signals import save_user