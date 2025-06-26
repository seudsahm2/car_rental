from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Car, CarCategory
from .serializers import CarSerializer, CarCategorySerializer

class CarListView(generics.ListAPIView):
    queryset = Car.objects.filter(is_active=True)
    serializer_class = CarSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'insurance_included', 'usdt_accepted']
    search_fields = ['make', 'model']

class CarDetailView(generics.RetrieveAPIView):
    queryset = Car.objects.filter(is_active=True)
    serializer_class = CarSerializer
    lookup_field = 'slug'

class CarCategoryListView(generics.ListAPIView):
    queryset = CarCategory.objects.all()
    serializer_class = CarCategorySerializer