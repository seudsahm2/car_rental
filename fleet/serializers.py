from rest_framework import serializers
from .models import Car, CarCategory, ImageGallery, PricingTier

class CarCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CarCategory
        fields = ['id', 'name', 'slug']

class ImageGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageGallery
        fields = ['id', 'image_path', 'caption', 'is_featured']

class PricingTierSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricingTier
        fields = ['id', 'name', 'multiplier']

class CarSerializer(serializers.ModelSerializer):
    category = CarCategorySerializer(read_only=True)
    gallery_images = ImageGallerySerializer(many=True, read_only=True)
    pricing_tiers = PricingTierSerializer(many=True, read_only=True)

    class Meta:
        model = Car
        fields = [
            'id', 'make', 'model', 'year', 'category', 'daily_rate', 'monthly_rate',
            'image_path', 'description', 'seats', 'insurance_included', 'usdt_accepted',
            'whatsapp_deal', 'no_security_deposit', 'slug', 'gallery_images', 'pricing_tiers',
            'luggage_capacity', 'doors', 'passengers', 'security_deposit', 'mileage_limit',
            'additional_km_rate'
        ]