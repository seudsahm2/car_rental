from django.contrib import admin  
from .models import HomepageHero, FAQ, BlogPost, Testimonial, AdPlacement  

@admin.register(HomepageHero)  
class HomepageHeroAdmin(admin.ModelAdmin):  
    list_display = ['title', 'is_active', 'order']  
    list_editable = ['is_active', 'order']  

@admin.register(FAQ)  
class FAQAdmin(admin.ModelAdmin):  
    list_display = ['question', 'category', 'is_active', 'order']  
    list_filter = ['category', 'is_active']  
    list_editable = ['is_active', 'order']  

@admin.register(BlogPost)  
class BlogPostAdmin(admin.ModelAdmin):  
    list_display = ['title', 'category', 'is_active', 'published_at']  
    list_filter = ['category', 'is_active']  
    prepopulated_fields = {'slug': ['title']}  

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating', 'is_featured', 'order']
    list_editable = ['is_featured', 'order']
    list_filter = ['rating', 'is_featured']
    search_fields = ['name', 'review']

@admin.register(AdPlacement)
class AdPlacementAdmin(admin.ModelAdmin):
    list_display = ['name', 'ad_slot_id', 'page', 'is_active']
    list_filter = ['page', 'is_active']
    list_editable = ['is_active']