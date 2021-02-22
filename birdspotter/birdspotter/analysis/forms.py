from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from birdspotter.analysis.models import Algorithm

class QueueJobForm(forms.Form):
    """Form for the import page

    Attributes:
        created_date (datetime.date): Date when the observation occurred
        file_to_import (File): File that will be saved into fileserver and read into database
        """  
    algorithm = forms.ModelChoiceField(Algorithm.objects.all(),empty_label="(Choose Algorithm)")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'queue-form'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn btn-primary'))