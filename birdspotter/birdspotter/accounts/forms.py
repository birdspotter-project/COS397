from django.forms import ModelForm, Textarea
from django import forms
from django.contrib.auth.forms import UserCreationForm


from .models import User, GroupRequest


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
        
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(f"Username {username} is already in use.")

    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()


class GroupRequestForm(forms.ModelForm):
    class Meta:
        model = GroupRequest
        fields = ('group', 'notes')
        widgets = {
            'notes': Textarea(attrs={'cols': 80, 'rows': 10}),
        }
        labels = {
            'notes': 'More details pertaining to the request'
        }