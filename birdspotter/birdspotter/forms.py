from django.forms import ModelForm
from birdspotter.dataio.models import Dataset

class DatasetEditForm(ModelForm):
    """
    Dataset metadata editing form 
    """
    class Meta:
        model = Dataset
        fields = ['name','comments','isPublic']