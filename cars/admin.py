from django.contrib import admin
from django.utils.html import format_html
from .models import Car, CarCategory,CarImage,Location, FAQ, FAQCategory,ContentSection,CustomerReview,SiteInfo,AdUnit
from .utils.supabase_client import get_supabase_client
from django import forms
from django.conf import settings
import os
# Inline for FAQs under FAQCategory
class FAQInline(admin.TabularInline):
    model = FAQ
    extra = 1
    fields = ['question', 'answer', 'slug', 'order']
    prepopulated_fields = {'slug': ('question',)}
    ordering = ['order']
@admin.register(CarCategory)
class CarCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'address']
    search_fields = ['name']

class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1
    fields = ['image_path', 'is_primary']

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'image_path':
            return forms.FileField(label='Image', required=False)
        return super().formfield_for_dbfield(db_field, **kwargs)

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['make', 'model', 'year', 'category', 'daily_rate', 'image_preview', 'no_security_deposit', 'whatsapp_deal']
    list_filter = ['category', 'year', 'insurance_included', 'usdt_accepted', 'no_security_deposit']
    search_fields = ['make', 'model', 'description']
    prepopulated_fields = {'slug': ('make', 'model', 'year')}
    list_editable = ['daily_rate', 'no_security_deposit', 'whatsapp_deal']
    inlines = [CarImageInline]

    fieldsets = (
        (None, {'fields': ('make', 'model', 'year', 'category', 'daily_rate', 'monthly_rate', 'slug')}),
        ('Details', {'fields': ('description', 'seats', 'luggage_capacity', 'doors', 'passengers', 'image_path')}),
        ('Features', {'fields': ('insurance_included', 'usdt_accepted', 'whatsapp_deal', 'no_security_deposit')}),
        ('Pricing', {'fields': ('security_deposit', 'mileage_limit', 'additional_km_rate')}),
    )

    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image_path:
            remote_db = os.getenv('REMOTE_DB', 'False').lower() in ('true', '1', 'yes')
            if remote_db:
                return format_html(
                    '<img src="{}/storage/v1/object/public/car-images/{}" style="max-height: 100px;" />',
                    settings.SUPABASE_URL, obj.image_path
                )
            return format_html(
                '<img src="{}" style="max-height: 100px;" />',
                f"{settings.MEDIA_URL}{obj.image_path}"
            )
        return "No Image"
    image_preview.short_description = 'Image'

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'image_path':
            return forms.FileField(label='Main Image', required=False)
        return super().formfield_for_dbfield(db_field, **kwargs)

    def save_model(self, request, obj, form, change):
        remote_db = os.getenv('REMOTE_DB', 'False').lower() in ('true', '1', 'yes')
        if 'image_path' in form.changed_data and request.FILES.get('image_path'):
            image_file = request.FILES['image_path']
            file_name = f"{obj.slug}-{image_file.name}"
            if remote_db:
                supabase = get_supabase_client()
                supabase.storage.from_('car-images').upload(file_name, image_file.read())
                obj.image_path = file_name
            else:
                os.makedirs(settings.MEDIA_ROOT, exist_ok=True)  # Create media directory if it doesn't exist
                file_path = os.path.join(settings.MEDIA_ROOT, file_name)
                with open(file_path, 'wb') as f:
                    f.write(image_file.read())
                obj.image_path = file_name
        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        remote_db = os.getenv('REMOTE_DB', 'False').lower() in ('true', '1', 'yes')
        for formset in formsets:
            if formset.model == CarImage:
                for form in formset:
                    if form.cleaned_data and form.cleaned_data.get('image_path'):
                        image_file = form.cleaned_data['image_path']
                        instance = form.instance
                        if isinstance(image_file, forms.FileField) or hasattr(image_file, 'read'):
                            file_name = f"{instance.car.slug}-inline-{image_file.name}"
                            if remote_db:
                                supabase = get_supabase_client()
                                supabase.storage.from_('car-images').upload(file_name, image_file.read())
                                instance.image_path = file_name
                            else:
                                os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
                                file_path = os.path.join(settings.MEDIA_ROOT, file_name)
                                with open(file_path, 'wb') as f:
                                    f.write(image_file.read())
                                instance.image_path = file_name
                        instance.save()@admin.register(FAQCategory)
class FAQCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [FAQInline]

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'order']
    list_filter = ['category']
    search_fields = ['question', 'answer']
    prepopulated_fields = {'slug': ('question',)}
    list_editable = ['order']
    list_per_page = 20
    
    fieldsets = (
        (None, {
            'fields': ('question', 'answer', 'category', 'slug', 'order')
        }),
    )


@admin.register(ContentSection)
class ContentSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'page', 'order']
    list_filter = ['page']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['order']
    list_per_page = 20
    
    fieldsets = (
        (None, {'fields': ('title', 'content', 'page', 'slug', 'order')}),
    )
    
@admin.register(CustomerReview)
class CustomerReviewAdmin(admin.ModelAdmin):
    list_display = ['name', 'review_preview', 'order']
    search_fields = ['name', 'review']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['order']
    list_per_page = 20
    fieldsets = (
        (None, {'fields': ('name', 'review', 'slug', 'order')}),
    )
    
    def review_preview(self, obj):
        return obj.review[:50] + ('...' if len(obj.review) > 50 else '')
    review_preview.short_description = 'Review'
    
@admin.register(SiteInfo)
class SiteInfoAdmin(admin.ModelAdmin):
    list_display = ['phone', 'email', 'hours']
    fieldsets = (
        (None, {'fields': ('phone', 'email', 'address', 'hours')}),
    )
    
    def has_add_permission(self, request):
        return not SiteInfo.objects.exists()
    
@admin.register(AdUnit)
class AdUnitAdmin(admin.ModelAdmin):
    list_display = ['name', 'page', 'is_active', 'updated_at']
    list_filter = ['page', 'is_active']
    search_fields = ['name', 'ad_slot']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active']
    list_per_page = 20
    fieldsets = (
        (None, {'fields': ('name', 'ad_slot', 'page', 'is_active', 'slug')}),
    )