from rest_framework import generics, filters  
from django_filters.rest_framework import DjangoFilterBackend  
from .models import BookingRequest, ContactInquiry  
from .serializers import BookingRequestSerializer, ContactInquirySerializer  

class BookingRequestListView(generics.ListAPIView):  
    queryset = BookingRequest.objects.all()  
    serializer_class = BookingRequestSerializer  
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]  
    filterset_fields = ['status']  
    ordering_fields = ['submitted_at']  

class ContactInquiryListView(generics.ListAPIView):
    queryset = ContactInquiry.objects.all()
    serializer_class = ContactInquirySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['is_resolved']
    ordering_fields = ['submitted_at']
    search_fields = ['name', 'phone', 'email']