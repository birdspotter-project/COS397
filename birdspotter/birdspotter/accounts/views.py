from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound


from .forms import AccountForm
from .models import User


def login_view(request):
    """Login view that is displayed in the nav bar
    when a user is not authenticated

    Args:
            request (HTTPRequest): api request

    Returns:
            Attempts to authenticate user and
            redirects to the application index
    """
    if request.method == 'POST':
        if user := authenticate(request, 
                                username=request.POST['username'],
                                password=request.POST['password']):
            login(request, user)
    return redirect('/')


def logout_view(request):
    logout(request)
    return redirect('/')


@login_required
def account_view(request):
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return render(request, 'success.html',
                          {'redirect': '/accounts/profile/'})

    form = AccountForm(initial={
        'username': request.user.username,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email,
    })
    return render(request, 'account.html', {'form': form})
