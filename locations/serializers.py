from rest_framework import serializers  
from .models import Location, LocationSpecificDeal, PricingTier  

class PricingTierSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = PricingTier  
        fields = ['id', 'name', 'multiplier', 'is_active']  

class LocationSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = Location  
        fields = ['id', 'name', 'slug', 'description', 'google_maps_embed_url', 'is_active']  

class LocationSpecificDealSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)
    pricing_tiers = PricingTierSerializer(many=True, read_only=True)
    # Dynamic resolution of `featured_cars` using ContentType (no direct import of `Car`)
    featured_cars = serializers.SerializerMethodField()

    def get_featured_cars(self, obj):
        from django.contrib.contenttypes.models import ContentType
        if obj.featured_cars_content_type and obj.featured_cars_object_ids:
            model_class = ContentType.objects.get_for_id(obj.featured_cars_content_type.id).model_class()
            cars = model_class.objects.filter(id__in=obj.featured_cars_object_ids)
            # Use a generic serializer or return minimal data
            return [{"id": car.id, "name": str(car)} for car in cars]
        return []

    class Meta:
        model = LocationSpecificDeal
        fields = [
            'id', 'title', 'subtitle', 'location', 'description',
            'is_active', 'order', 'slug', 'pricing_tiers', 'featured_cars'
        ]