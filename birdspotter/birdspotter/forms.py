from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from birdspotter.dataio.models import Dataset

class DatasetEditForm(ModelForm):
    """
    Dataset metadata editing form, using ModelForm
    """
    class Meta:
        model = Dataset
        fields = ['name','comments','is_public']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'queue-form'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn btn-primary'))