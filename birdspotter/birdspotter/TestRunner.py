from django.conf import settings
from django.test.runner import DiscoverRunner

class TestRunner(DiscoverRunner):
    def __init__(self, *args, **kwargs):
        settings.TESTING = True
        super(TestRunner, self).__init__(*args, **kwargs)