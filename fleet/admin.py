from django.contrib import admin
from django.utils.html import format_html
from .models import Car, CarCategory, ImageGallery, MaintenanceLog,PricingTier
from django import forms
from .forms import ImageGalleryInlineForm
from django.core.exceptions import ValidationError
from utils.supabase_client import get_supabase_client
import os
import time
import logging
from django.conf import settings
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet

logging.getLogger('supabase').setLevel(logging.WARNING)
logging.getLogger('httpcore').setLevel(logging.WARNING)
logging.getLogger('httpx').setLevel(logging.WARNING)

def validate_file_size(file, max_size=5*1024*1024):  # 5MB limit
    if file.size > max_size:
        raise ValidationError(f"File size must be under {max_size/(1024*1024)}MB")

# formset.py or inline admin file

class ImageGalleryInlineFormset(BaseInlineFormSet):
    def clean(self):
        super().clean()
        selected_found = False

        for form in self.forms:
            if not hasattr(form, 'cleaned_data') or form.cleaned_data.get('DELETE', False):
                continue

            if form.cleaned_data.get('is_primary'):
                if selected_found:
                    raise ValidationError("Only one image can be marked as primary.")
                selected_found = True
                form.cleaned_data['is_primary'] = True
            else:
                form.cleaned_data['is_primary'] = False

        if not selected_found and any(not f.cleaned_data.get('DELETE', False) for f in self.forms):
            raise ValidationError("Please select one primary image.")



class ImageGalleryInline(admin.TabularInline):
    model = ImageGallery
    form = ImageGalleryInlineForm
    formset = ImageGalleryInlineFormset
    extra = 1
    fields = ['image_path', 'caption', 'is_primary', 'order', 'image_preview']
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image_path:
            return format_html(
                '<img src="{}{}" style="max-height: 100px;" />',
                settings.MEDIA_URL, obj.image_path
            )
        return "No Image"

    image_preview.short_description = "Preview"

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'image_path':
            field = forms.FileField(label='Image', required=False)
            field.validators.append(validate_file_size)
            return field
        return super().formfield_for_dbfield(db_field, **kwargs)

class MaintenanceLogInline(admin.TabularInline):
    model = MaintenanceLog
    extra = 1

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = [
        'make', 'model', 'year', 'category', 'daily_rate',
        'primary_image_preview',  # <-- show this
        'no_security_deposit', 'whatsapp_deal'
    ]
    list_filter = ['category', 'insurance_included', 'usdt_accepted']
    search_fields = ['make', 'model']
    inlines = [ImageGalleryInline, MaintenanceLogInline]
    prepopulated_fields = {'slug': ['make', 'model', 'year']}

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        remote_db = os.getenv('REMOTE_DB', 'False').lower() in ('true', '1', 'yes')
        for formset in formsets:
            if formset.model == ImageGallery:
                for form in formset:
                    if form.cleaned_data and form.cleaned_data.get('image_path'):
                        image_file = form.cleaned_data['image_path']
                        instance = form.instance
                        if hasattr(image_file, 'read'):
                            timestamp = int(time.time())
                            file_name = f"{instance.car.slug}-inline-{timestamp}-{image_file.name}"
                            if remote_db:
                                supabase = get_supabase_client()
                                image_data = image_file.read()
                                supabase.storage.from_('car-images').upload(file_name, image_data, file_options={'content-type': image_file.content_type})
                                instance.image_path = file_name
                            else:
                                os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
                                file_path = os.path.join(settings.MEDIA_ROOT, file_name)
                                with open(file_path, 'wb') as f:
                                    for chunk in image_file.chunks():
                                        f.write(chunk)
                                instance.image_path = file_name
                            instance.save()
    
    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        for formset in formsets:
            if formset.model == ImageGallery:
                for form in formset:
                    if form.cleaned_data and form.cleaned_data.get('image_path'):
                        image_file = form.cleaned_data['image_path']
                        instance = form.instance

                        if hasattr(image_file, 'read'):
                            # Save to local file system
                            timestamp = int(time.time())
                            filename = f"{instance.car.slug}-img-{timestamp}-{image_file.name}"
                            full_path = os.path.join(settings.MEDIA_ROOT, filename)

                            os.makedirs(os.path.dirname(full_path), exist_ok=True)
                            with open(full_path, 'wb') as f:
                                for chunk in image_file.chunks():
                                    f.write(chunk)

                            instance.image_path = filename  # Save path to DB
                            instance.save()
    
    def primary_image_preview(self, obj):
        primary = obj.gallery_images.filter(is_primary=True).first()
        if primary and primary.image_path:
            remote_db = os.getenv('REMOTE_DB', 'False').lower() in ('true', '1', 'yes')
            image_url = (
                f"{settings.SUPABASE_URL}/storage/v1/object/public/car-images/{primary.image_path}"
                if remote_db else
                f"{settings.MEDIA_URL}{primary.image_path}"
            )
            return format_html('<img src="{}" style="max-height: 50px;" />', image_url)
        return "No Image"

    primary_image_preview.short_description = "Preview"
    class Media:
        js = ('admin/js/image_radio_fix.js',)

@admin.register(CarCategory)
class CarCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ['name']}
@admin.register(PricingTier)
class PricingTierAdmin(admin.ModelAdmin):
    list_display = ['name', 'multiplier', 'is_active']
    list_editable = ['is_active']