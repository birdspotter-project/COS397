from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import AccountForm


def login_view(request):
	if request.method == 'POST':
		if user := authenticate(request, username=request.POST['username'], password=request.POST['password']):
			login(request, user)	
			return redirect('/')
		else:
			return redirect('/')
	return redirect('/')

def logout_view(request):
	logout(request)
	return redirect('/')

@login_required
def account_view(request):
	form = AccountForm()
	context = {
		'form': form
	}
	return render(request, 'account.html', context)