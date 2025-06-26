from rest_framework import serializers
from .models import BookingRequest, ContactInquiry

class BookingRequestSerializer(serializers.ModelSerializer):
    # Dynamically resolve the `car` field using GenericForeignKey
    car = serializers.SerializerMethodField()

    def get_car(self, obj):
        if not obj.car:
            return None
        return {
            "id": obj.car.id,
            "name": f"{obj.car.make} {obj.car.model}",
        }

    class Meta:
        model = BookingRequest
        fields = [
            'id', 'car', 'name', 'phone', 'pickup_date', 'return_date',
            'message', 'submitted_at', 'status'
        ]

class ContactInquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInquiry
        fields = [
            'id', 'name', 'phone', 'email', 'message',
            'submitted_at', 'is_resolved'
        ]