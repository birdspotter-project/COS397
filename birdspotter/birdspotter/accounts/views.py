from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import (AccountForm,
                    RegisterForm,
                    GroupRequestForm,
                    ContactForm,
                    )
from .models import GroupRequest
from .scripts import send_email_to_admins


REQUESTS = {
    'success': 'Request created successfully. Please wait for an admin to approve your request',
    'error': 'Error creating request, please try again later.'
}


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
            messages.success(request, f"Welcome, {user.username}!")
        else:
            messages.error(request, "Login failed.")
    return redirect('/')


def logout_view(request):
    """ View that logs the current user out of the application and redirects
    to the application index
    """
    logout(request)
    return redirect('/')

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            success = send_email_to_admins(form.cleaned_data['subject'],
                                form.cleaned_data['message'],
                                from_email=form.cleaned_data['email'])
            if success:
                messages.success(request, 'Email sent successfully')
            else:
                messages.error(request, 'Error sending email, please try again')
            return redirect('/contact')
    form = ContactForm(initial={
        'email': request.user.email if request.user.is_authenticated else ''
    })
    return render(request, 'contact.html', {'form': form})


@login_required
def account_view(request):
    """ View where a logged in user can view their account information and also
    change some information via an AccountForm
    """
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
    """ View where the user registers for an account in the system
    Upon submitting, a GroupRequest is created and an admin is notified of
    the request. The user cannot log into the system until that request is
    approved.
    """
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user:
                user.is_active = False
                user.save()
                group_request = GroupRequest(user=user)
                group_request.save()
                messages.success(request, REQUESTS['success'])
            else:
                messages.error(request, REQUESTS['error'])
            return redirect('/')
    return render(request, 'registration/register_user.html', {'form': form})


@login_required
def request_privileged_view(request):
    """ View where a logged in user can request a different permissions group
    via a GroupRequestForm. Once the form is submitted, a GroupRequest is
    created and an admin is notified of the request
    """
    if request.method == 'POST':
        form = GroupRequestForm(request.POST)
        if form.is_valid():
            group_request = form.save(commit=False)
            group_request.user = request.user
            group_request.save()
            if group_request:
                messages.success(request, REQUESTS['success'])
            else:
                messages.error(request, REQUESTS['error'])
    form = GroupRequestForm(initial={'user': request.user})
    return render(request, 'request_group.html', {'form': form})


@login_required
@staff_member_required
def group_request_view(request):
    """ View where a logged in staff member (Admin) can view and take action
    on group requests.
    """
    group_requests = GroupRequest.objects.filter(approved=False).filter(reviewed_by__isnull=True)
    return render(request, 'group_requests.html', {'group_requests': group_requests})


@login_required
@staff_member_required
def process_request_action(request, request_id, action):
    """ View that accepts requests from the group_request_view, and performs
    the associated action, whether that be accepting the request of denying it.
    For actions to occur, the user must be logged in and a member of staff (Admin)
    """
    group_request = GroupRequest.objects.get(request_id=request_id)
    if action == 'approve':
        group_request.approve_request(request)
    elif action == 'deny':
        group_request.deny_request(request)
    else:
        messages.error(request, 'There was an error %sing the request' % action)
        return HttpResponse(status=500)
    return HttpResponse(status=200)
