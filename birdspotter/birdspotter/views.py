from django.shortcuts import render
from django.http import HttpResponse
from birdspotter.dataio.scripts.get_user_datasets import get_datasets_for_user
from birdspotter.accounts.models import User

def index(request):
	u = None
	try:
		u = User.objects.get_by_natural_key('testUser')
	except:
		u = User(username='testUser')
		u.save()
	print(request.user.is_authenticated)
	datasets = get_datasets_for_user(u).values()
	return render(request, 'index.html', {'datasets': datasets})