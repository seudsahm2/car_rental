from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import Car, CarCategory, ImageGallery, MaintenanceLog, PricingTier

class ImageGalleryInline(admin.TabularInline):
    model = ImageGallery
    extra = 1

class MaintenanceLogInline(admin.TabularInline):
    model = MaintenanceLog
    extra = 1

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['make', 'model', 'year', 'daily_rate', 'is_active']
    list_filter = ['category', 'insurance_included', 'usdt_accepted']
    search_fields = ['make', 'model']
    inlines = [ImageGalleryInline, MaintenanceLogInline]
    prepopulated_fields = {'slug': ['make', 'model', 'year']}

@admin.register(CarCategory)
class CarCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ['name']}

@admin.register(PricingTier)
class PricingTierAdmin(admin.ModelAdmin):
    list_display = ['name', 'multiplier', 'is_active']
    list_editable = ['is_active']