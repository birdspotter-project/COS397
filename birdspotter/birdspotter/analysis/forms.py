from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class ImportShapefileForm(forms.Form):
    """Form for the import page

    Attributes:
        created_date (datetime.date): Date when the observation occurred
        file_to_import (File): File that will be saved into fileserver and read into database
        """
    created_date = forms.DateField(
        widget=forms.TextInput(     
            attrs={'type': 'date'} 
        )
    )
    file_to_import = forms.FileField(label=".zip file to import")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'upload-form'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn btn-primary'))
