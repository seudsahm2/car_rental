from rest_framework import serializers
from .models import Car, CarCategory,FAQCategory,FAQ,ContentSection

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

class CarSerializer(serializers.ModelSerializer):
    category = CarCategorySerializer(read_only=True)
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Car
        fields = [
            'id',
            'make',
            'model',
            'year',
            'category',
            'daily_rate',
            'image_url',
            'description',
            'seats',
            'insurance_included',
            'usdt_accepted',
            'whatsapp_deal',
            'no_security_deposit',  # Added to serializer
            'slug',
            'created_at'
        ]
    
    def get_image_url(self, obj):
        request = self.context.get(('request'), 'pass')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url)
        return None