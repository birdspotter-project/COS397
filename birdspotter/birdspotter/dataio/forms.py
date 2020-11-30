from django import forms

class ImportShapefileForm(forms.Form):
	created_date = forms.DateField()
	file_to_import = forms.FileField()