from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout

from .forms import LoginForm


def login_view(request):
	if request.method == 'POST':
		if user := authenticate(request, username=request.POST['username'], password=request.POST['password']):
			login(request, user)	
			print('User %s logged in successfully' % user.username)
		return redirect('/')
	else:
		form = LoginForm()
		return render('/', {'form': form})
	return render(request, 'login.html')

def logout_view(request):
	logout(request)
	return redirect('/')