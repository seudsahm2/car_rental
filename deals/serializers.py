from rest_framework import serializers  
from .models import MonthlyRentalDeal, PromoBanner, ServiceBenefit  

class MonthlyRentalDealSerializer(serializers.ModelSerializer):  
    # Dynamically resolve the `car` field using GenericForeignKey  
    car = serializers.SerializerMethodField()  

    def get_car(self, obj):  
        return {  
            "id": obj.car.id,  
            "name": f"{obj.car.make} {obj.car.model}",  
            "daily_rate": obj.car.daily_rate,  
        }  

    class Meta:  
        model = MonthlyRentalDeal  
        fields = [  
            'id', 'car', 'discount_percentage', 'monthly_rate',  
            'promo_tag', 'terms', 'is_active', 'order'  
        ]  

class PromoBannerSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = PromoBanner  
        fields = [  
            'id', 'title', 'text', 'button_text', 'button_link',  
            'is_active', 'start_date', 'end_date'  
        ]  

class ServiceBenefitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceBenefit
        fields = ['id', 'title', 'icon', 'description', 'is_active', 'order']