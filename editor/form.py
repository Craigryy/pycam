# Create a form to handle image uploads.

from django import forms
from .models import ImageEdit

class ImageEditForm(forms.ModelForm):
    class Meta:
        model = ImageEdit
        fields = ['original_image']

