from django import forms


class ImportShapefileForm(forms.Form):
    """Form for the import page

    Attributes:
        created_date (datetime.date): Date when the observation occurred
        file_to_import (File): File that will be saved into fileserver and read into database
        """
    created_date = forms.DateField()
    file_to_import = forms.FileField(label=".zip file to import")
