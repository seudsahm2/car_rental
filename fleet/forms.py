from django import forms
from django.core.exceptions import ValidationError
from .models import ImageGallery

class ImageGalleryInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        super().clean()
        primary_count = 0
        has_valid_forms = False

        for form in self.forms:
            if not hasattr(form, 'cleaned_data') or form.cleaned_data.get('DELETE', False):
                continue
            has_valid_forms = True
            if form.cleaned_data.get('is_primary'):
                primary_count += 1

        if has_valid_forms and primary_count == 0:
            raise ValidationError("Please select one primary image.")
        if primary_count > 1:
            raise ValidationError("Only one image can be marked as primary.")

class ImageGalleryInlineForm(forms.ModelForm):
    is_primary = forms.BooleanField(
        widget=forms.RadioSelect(choices=[(True, 'Primary'), (False, '')]),
        required=False,
        label=''
    )

    class Meta:
        model = ImageGallery
        fields = '__all__'