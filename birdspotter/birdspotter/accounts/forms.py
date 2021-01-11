from django.forms import ModelForm
from .models import User

class AccountForm(ModelForm):
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email']

		def __init__(self, *args, **kwargs):
			super(YourModelForm, self).__init__(*args, **kwargs)
			for field_name, field in self.fields.items():
				print(field.widget)
				if field.widget.attrs.get('class'):
					field.widget.attrs['class'] += ' form-control'
				else:
					field.widget.attrs['class']='form-control'