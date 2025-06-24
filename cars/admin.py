from django.contrib import admin
from django.utils.html import format_html
from .models import Car, CarCategory, FAQ, FAQCategory,ContentSection,CustomerReview

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
        (None, {
            'fields': ('make', 'model', 'year', 'category', 'daily_rate', 'slug')
        }),
        ('Details', {
            'fields': ('description', 'seats', 'image')
        }),
        ('Features', {
            'fields': ('insurance_included', 'usdt_accepted', 'whatsapp_deal', 'no_security_deposit')
        }),
    )
    
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Image'

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