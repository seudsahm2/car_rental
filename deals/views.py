from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import MonthlyRentalDeal, PromoBanner, ServiceBenefit
from .serializers import (
    MonthlyRentalDealSerializer,
    PromoBannerSerializer,
    ServiceBenefitSerializer
)

class MonthlyRentalDealListView(generics.ListAPIView):
    queryset = MonthlyRentalDeal.objects.filter(is_active=True)
    serializer_class = MonthlyRentalDealSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['discount_percentage']
    ordering_fields = ['order', 'monthly_rate']

class PromoBannerListView(generics.ListAPIView):
    queryset = PromoBanner.objects.filter(is_active=True)
    serializer_class = PromoBannerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_active']

class ServiceBenefitListView(generics.ListAPIView):
    queryset = ServiceBenefit.objects.filter(is_active=True)
    serializer_class = ServiceBenefitSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_active']
    ordering_fields = ['order']