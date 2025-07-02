from rest_framework import serializers
from .models import Car, CarCategory,CarImage,Location,FAQCategory,FAQ,ContentSection,CustomerReview,SiteInfo,AdUnit
from django.conf import settings
import os
# Serializers
class ContentSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentSection
        fields = ['id', 'title', 'content', 'slug', 'page', 'order']
class FAQCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQCategory
        fields = ['id', 'name', 'slug']

class FAQSerializer(serializers.ModelSerializer):
    category = FAQCategorySerializer(read_only=True)
    
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer', 'category', 'slug', 'order']

class CarCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CarCategory
        fields = ['id', 'name', 'slug']

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name', 'address']

class CarImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = CarImage
        fields = ['id', 'image_url', 'is_primary']

    def get_image_url(self, obj):
        if obj.image_path:
            remote_db = os.getenv('REMOTE_DB', 'False').lower() in ('true', '1', 'yes')
            if remote_db:
                return f"{settings.SUPABASE_URL}/storage/v1/object/public/car-images/{obj.image_path}"
            return f"{settings.MEDIA_URL}{obj.image_path}"
        return None

class CarSerializer(serializers.ModelSerializer):
    category = CarCategorySerializer(read_only=True)
    image_url = serializers.SerializerMethodField()
    images = CarImageSerializer(many=True, read_only=True)
    related_cars = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = [
            'id', 'make', 'model', 'year', 'category', 'daily_rate', 'monthly_rate', 'image_url',
            'description', 'seats', 'insurance_included', 'usdt_accepted', 'whatsapp_deal',
            'no_security_deposit', 'slug', 'created_at', 'luggage_capacity', 'doors', 'passengers',
            'security_deposit', 'mileage_limit', 'additional_km_rate', 'images', 'related_cars'
        ]

    def get_image_url(self, obj):
        if obj.image_path:
            remote_db = os.getenv('REMOTE_DB', 'False').lower() in ('true', '1', 'yes')
            if remote_db:
                return f"{settings.SUPABASE_URL}/storage/v1/object/public/car-images/{obj.image_path}"
            return f"{settings.MEDIA_URL}{obj.image_path}"
        return None

    def get_related_cars(self, obj):
        related = Car.objects.filter(category=obj.category).exclude(id=obj.id)[:3]
        # Use the lightweight serializer here
        return RelatedCarSerializer(related, many=True, context=self.context).data

    
class RelatedCarSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = [
            'id', 'make', 'model', 'year', 'image_url', 'daily_rate', 'slug'
        ]

    def get_image_url(self, obj):
        if obj.image_path:
            remote_db = os.getenv('REMOTE_DB', 'False').lower() in ('true', '1', 'yes')
            if remote_db:
                return f"{settings.SUPABASE_URL}/storage/v1/object/public/car-images/{obj.image_path}"
            return f"{settings.MEDIA_URL}{obj.image_path}"
        return None

class CustomerReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerReview
        fields = ['id', 'name', 'review', 'slug', 'created_at', 'order']
        
class SiteInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteInfo
        fields = ['id', 'phone', 'email', 'address', 'hours']
    
class AdUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdUnit
        fields = ['id', 'name', 'ad_slot', 'page', 'is_active', 'slug', 'created_at', 'updated_at']