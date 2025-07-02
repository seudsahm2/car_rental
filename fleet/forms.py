# forms.py
from django import forms
from .models import ImageGallery

class ImageGalleryInlineForm(forms.ModelForm):
    is_primary = forms.TypedChoiceField(
        choices=[('True', 'Primary')],  # Note string 'True'
        widget=forms.RadioSelect(attrs={'name': 'primary_image'}),
        required=False,
        coerce=lambda x: x == 'True',  # convert string 'True' to boolean True
        empty_value=False,
        label=''
    )

    class Meta:
        model = ImageGallery
        fields = '__all__'
