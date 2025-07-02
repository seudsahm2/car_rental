# fleet/__init__.py
from django import forms
from django.core.exceptions import ValidationError

class ImageGalleryInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        super().clean()
        primary_count = sum(
            1 for form in self.forms
            if form.cleaned_data.get('is_primary') and not form.cleaned_data.get('DELETE', False)
        )
        if primary_count > 1:
            raise ValidationError("Only one image can be marked as primary.")
        if not primary_count and any(
            form.cleaned_data and not form.cleaned_data.get('DELETE', False)
            for form in self.forms
        ):
            raise ValidationError("At least one image must be marked as primary if images are present.")
