from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm


from .models import User


class AccountForm(ModelForm):
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
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()


class RequestPrivilegedAccessForm(forms.Form):
    # TODO: redo this
    organization = forms.CharField(required=False)
    reason = forms.CharField(max_length=1000, required=True, label='Reason for elevated permissions', widget=forms.Textarea)
