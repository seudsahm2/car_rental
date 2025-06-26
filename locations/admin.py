from django.contrib import admin
from .models import Location, LocationSpecificDeal, PricingTier

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    prepopulated_fields = {'slug': ['name']}

@admin.register(LocationSpecificDeal)
class LocationSpecificDealAdmin(admin.ModelAdmin):
    list_display = ['title', 'location', 'is_active', 'order']
    list_filter = ['location', 'is_active']
    search_fields = ['title', 'location__name']
    prepopulated_fields = {'slug': ['title']}

@admin.register(PricingTier)
class PricingTierAdmin(admin.ModelAdmin):
    list_display = ['name', 'multiplier', 'is_active']
    list_editable = ['is_active']