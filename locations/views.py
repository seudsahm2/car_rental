from rest_framework import generics
from .models import Location, LocationSpecificDeal
from .serializers import LocationSerializer, LocationSpecificDealSerializer

class LocationListView(generics.ListAPIView):
    queryset = Location.objects.filter(is_active=True)
    serializer_class = LocationSerializer

class LocationDetailView(generics.RetrieveAPIView):
    queryset = Location.objects.filter(is_active=True)
    serializer_class = LocationSerializer
    lookup_field = 'slug'

class LocationSpecificDealListView(generics.ListAPIView):
    queryset = LocationSpecificDeal.objects.filter(is_active=True)
    serializer_class = LocationSpecificDealSerializer
    filter_fields = ['location']

class LocationSpecificDealDetailView(generics.RetrieveAPIView):
    queryset = LocationSpecificDeal.objects.filter(is_active=True)
    serializer_class = LocationSpecificDealSerializer
    lookup_field = 'slug'