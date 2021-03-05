from django.shortcuts import render
from birdspotter.dataio.scripts.get_user_datasets import get_datasets_for_user
from birdspotter.accounts.models import User
from django.http import HttpResponse


def index(request):
    """
    Application index which is also the landing page. This view displays a table with all datasets available to the
    currently authenticated user, otherwise, display only public facing datasets.
    """
    current_user = None
    try:
        current_user = User.objects.get_by_natural_key(request.user)
    except Exception:
        print('Could not find user: %s' % request.user.username)
    if current_user:
        datasets = get_datasets_for_user(current_user).values()
    else:
        datasets = None
    return render(request, 'index.html', {'datasets': datasets})


# How to correctly send a fully compliant HTTP 204 response, based on https://code.djangoproject.com/ticket/16632
class HttpResponseNoContent(HttpResponse):
    """Special HTTP response with no content, just headers.

    The content operations are ignored.
    """

    def __init__(self, content="", mimetype=None, status=None, content_type=None): # noqa
        super().__init__(status=204)

        if "content-type" in self._headers:
            del self._headers["content-type"]

    def _set_content(self, value):
        pass

    def _get_content(self, value):
        pass


def auth(request):
    """
    Used by NGINX to check if the user is authorized with minimal overhead.
    """
    if request.user.is_authenticated:
        return HttpResponseNoContent()
    return HttpResponse(status=403)