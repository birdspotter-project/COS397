from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages



from .forms import AccountForm, RegisterForm, RequestPrivilegedAccessForm


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
        form = AccountForm(request.POST)
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


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            args = {}
            user = form.save()
            if user:
                args = {
                    'statusDiv': 'Account created successfully',
                    'result': 'success',
                    'redirect': '/'
                }
            else:
                args = {
                    'statusDiv': 'Error creating account',
                    'result': 'danger',
                    'redirect': '/accounts/register/'
                }
            return render(request, 'result.html', args)
    form = RegisterForm()
    return render(request, 'registration/register_user.html', {'form': form})

@login_required
def request_privileged_view(request):
    if request.method == 'POST':
        form = RequestPrivilegedAccessForm(request.POST)
    form = RequestPrivilegedAccessForm()
    return render(request, 'request_group.html', {'form': form})