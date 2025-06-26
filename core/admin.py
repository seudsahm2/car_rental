from django.contrib import admin  
from .models import SiteConfiguration, SocialMediaLink, PageMeta, Language, Translation  

@admin.register(SiteConfiguration)  
class SiteConfigurationAdmin(admin.ModelAdmin):  
    def has_add_permission(self, request):  
        return not SiteConfiguration.objects.exists()  # Allow only one instance  

@admin.register(SocialMediaLink)  
class SocialMediaLinkAdmin(admin.ModelAdmin):  
    list_display = ['platform', 'url', 'is_active', 'order']  
    list_editable = ['is_active', 'order']  
    list_filter = ['platform', 'is_active']  

@admin.register(PageMeta)  
class PageMetaAdmin(admin.ModelAdmin):  
    list_display = ['page', 'title']  
    search_fields = ['page', 'title']  

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'is_active', 'is_default']
    list_editable = ['is_active', 'is_default']
    search_fields = ['name', 'code']

@admin.register(Translation)
class TranslationAdmin(admin.ModelAdmin):
    list_display = ['key', 'language', 'value']
    list_filter = ['language']
    search_fields = ['key', 'value']