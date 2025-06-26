from rest_framework import serializers
from .models import HomepageHero, FAQ, BlogPost, Testimonial, AdPlacement

class HomepageHeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomepageHero
        fields = ['id', 'title', 'subtitle', 'background_image_path', 'cta_text', 'cta_link', 'is_active', 'order']

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer', 'category', 'is_active', 'order']

class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'excerpt', 'content', 'featured_image',
            'category', 'published_at', 'is_active', 'order'
        ]

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ['id', 'name', 'review', 'rating', 'is_featured', 'order', 'created_at']

class AdPlacementSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdPlacement
        fields = ['id', 'name', 'ad_slot_id', 'page', 'is_active']