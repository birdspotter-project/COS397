from django.apps import AppConfig

class AnalysisConfig(AppConfig):
    name = 'birdspotter.analysis'
    def ready(self):
        from .signals import handle_mail # noqa