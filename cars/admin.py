from django import forms
from django.contrib import admin
from django.utils.html import format_html
from .models import Car

class CarAdminForm(forms.ModelForm):
    features_input = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        help_text="Enter one feature per line",
        required=False
    )
    
    class Meta:
        model = Car
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.features:
            self.initial['features_input'] = "\n".join(self.instance.features)
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        features = self.cleaned_data['features_input'].split("\n")
        instance.features = [f.strip() for f in features if f.strip()]
        if commit:
            instance.save()
        return instance

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    form = CarAdminForm
    list_display = ('title', 'price', 'year', 'category', 'available', 'image_preview')
    list_filter = ('category', 'available')
    search_fields = ('title', 'features')
    list_editable = ('available',)
    readonly_fields = ('image_preview',)
    
    fieldsets = (
        (None, {
            'fields': ('title', 'price', 'year', 'category', 'features_input')
        }),
        ('Contact Information', {
            'fields': ('whatsapp_number', 'call_number')
        }),
        ('Images', {
            'fields': ('image', 'image_preview')
        }),
        ('Status', {
            'fields': ('available',)
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Preview'

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Remove the original features field from the form since we're using features_input
        if 'features' in form.base_fields:
            del form.base_fields['features']
        return form