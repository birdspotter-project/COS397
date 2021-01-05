from django.shortcuts import render
from django.http import HttpResponse
from birdspotter.dataio.scripts.get_user_datasets import get_datasets_for_user
from birdspotter.accounts.models import User

def index(request):
	"""
	Application index which is also the landing page. This view displays a table with all datasets available to the
	currently authenticated user, otherwise, display only public facing datasets.
	"""
	current_user = None
	try:
		current_user = User.objects.get_by_natural_key(request.user)
	except Exception as e:
		print(e)
	print(request.user.is_authenticated)
	if current_user:
		datasets = get_datasets_for_user(current_user).values()
	else:
		datasets = None
	return render(request, 'index.html', {'datasets': datasets})