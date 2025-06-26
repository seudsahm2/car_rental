from django.contrib import admin
from .models import MonthlyRentalDeal, PromoBanner, ServiceBenefit

@admin.register(MonthlyRentalDeal)
class MonthlyRentalDealAdmin(admin.ModelAdmin):
    list_display = ['car', 'discount_percentage', 'monthly_rate', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    list_filter = ['is_active']
    search_fields = ['car__make', 'car__model']

@admin.register(PromoBanner)
class PromoBannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'start_date', 'end_date']
    list_editable = ['is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'text']

@admin.register(ServiceBenefit)
class ServiceBenefitAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    list_filter = ['is_active']
    search_fields = ['title']