from django.forms import ModelForm, Textarea
from django import forms
from django.contrib.auth.forms import UserCreationForm


from .models import User, GroupRequest


class AccountForm(ModelForm):
    """ Form for displaying and editing a User's account information.
    This is a ModelForm based off the User model in birdspotter.accounts.models
    """
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for _, field in self.fields.items():
                if field.widget.attrs.get('class'):
                    field.widget.attrs['class'] += ' form-control'
                else:
                    field.widget.attrs['class'] = 'form-control'

class RegisterForm(UserCreationForm):
    """ Registration form for a user to register for an account in the application

    Attributes:
        email (str): the user's desired email address
        first_name (str): the user's first name
        last_name (str): the user's last name
    """
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()


class GroupRequestForm(forms.ModelForm):
    """ Form for a user to request permissions within the system
    This form displays a choice field where a user can select the desirted permission level
    and provide any information that would like to add to the request.
    """
    class Meta:
        model = GroupRequest
        fields = ('group', 'notes')
        widgets = {
            'notes': Textarea(attrs={'cols': 80, 'rows': 10}),
        }
        labels = {
            'notes': 'More details pertaining to the request'
        }