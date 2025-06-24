from django.contrib import admin
from django.utils.html import format_html
from .models import Car, CarCategory, FAQ, FAQCategory,ContentSection,CustomerReview,SiteInfo,AdUnit
from .utils.supabase_client import get_supabase_client
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
    list_filter = ['name']
    
    fieldsets = (
        (None, {
            'fields': ('name', 'slug')
        }),
    )

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['make', 'model', 'year', 'category', 'daily_rate', 'image_preview', 'no_security_deposit', 'whatsapp_deal']
    list_filter = ['category', 'year', 'insurance_included', 'usdt_accepted', 'no_security_deposit']
    search_fields = ['make', 'model', 'description']
    prepopulated_fields = {'slug': ('make', 'model', 'year')}
    list_editable = ['daily_rate', 'no_security_deposit', 'whatsapp_deal']
    list_per_page = 20

    fieldsets = (
        (None, {'fields': ('make', 'model', 'year', 'category', 'daily_rate', 'slug')}),
        ('Details', {'fields': ('description', 'seats', 'image_path')}),
        ('Features', {'fields': ('insurance_included', 'usdt_accepted', 'whatsapp_deal', 'no_security_deposit')}),
    )

    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image_path:
            return format_html('<img src="{}/storage/v1/object/public/car-images/{}" style="max-height: 100px;" />',
                               settings.SUPABASE_URL, obj.image_path)
        return "No Image"
    image_preview.short_description = 'Image'

    def save_model(self, request, obj, form, change):
        supabase = get_supabase_client()
        if 'image_path' in form.changed_data:
            image_file = form.cleaned_data['image_path']
            if image_file:
                file_name = f"{obj.slug}-{image_file.name}"
                supabase.storage.from_('car-images').upload(file_name, image_file.read())
                obj.image_path = file_name
        # Save to Supabase
        data = {
            'make': obj.make,
            'model': obj.model,
            'year': obj.year,
            'category_id': obj.category_id,
            'daily_rate': float(obj.daily_rate),
            'image_path': obj.image_path,
            'description': obj.description,
            'seats': obj.seats,
            'insurance_included': obj.insurance_included,
            'usdt_accepted': obj.usdt_accepted,
            'whatsapp_deal': obj.whatsapp_deal,
            'no_security_deposit': obj.no_security_deposit,
            'slug': obj.slug,
        }
        if change:
            supabase.table('cars').update(data).eq('id', obj.id).execute()
        else:
            supabase.table('cars').insert(data).execute()
        super().save_model(request, obj, form, change)

@admin.register(FAQCategory)
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