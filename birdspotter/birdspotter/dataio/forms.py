from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class NoInput(forms.Widget):
    input_type = "hidden"
    template_name = ""

    def render(self, name, value, attrs=None, renderer=None):
        return ""


class UploadedFileInput(forms.widgets.FileInput):
    input_type = 'file'
    needs_multipart_form = True
    template_name = 'django/forms/widgets/file.html'

    def format_value(self, value):
        """File input never renders a value."""
        return

    def value_from_datadict(self, data, files, name):
        "This special version gets data from DATA not FILES"
        return data.get(name)

    def value_omitted_from_data(self, data, files, name):
        return name not in data

    def use_required_attribute(self, initial):
        return super().use_required_attribute(initial) and not initial


class ImportForm(forms.Form):
    """Form for the import page

    Attributes:
        created_date (datetime.date): Date when the observation occurred
        file_to_import (File): File that will be saved into fileserver and read into database
        """
    file_path = forms.CharField(
        label=".zip or .tif file to import", 
        widget=UploadedFileInput)
    public = forms.BooleanField(required=False, initial=False, label='Make dataset public')
    file_md5 = forms.CharField(max_length=32, widget=NoInput)
    file_name = forms.CharField(max_length=64, widget=NoInput)
    file_size = forms.IntegerField(widget=NoInput)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'upload-form'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'POST'
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'
        self.helper.form_action = '/upload/'
        self.helper.add_input(Submit('submit', 'Submit'))
