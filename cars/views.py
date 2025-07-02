# cars/views.py

from rest_framework import generics, filters
from .models import Car, CarCategory,Location,FAQ,ContentSection,CustomerReview,SiteInfo,AdUnit
from .serializers import CarSerializer, CarCategorySerializer, CarCategorySerializer, LocationSerializer, FAQSerializer, ContentSectionSerializer,CustomerReviewSerializer,SiteInfoSerializer,AdUnitSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from django.http import HttpResponse
from django.contrib.auth.models import User
# Views
# C:\Users\hp\Downloads\Projects\Django\car_rental_backend\cars\views.py
from rest_framework import generics, filters
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import Car, CarCategory
from .serializers import CarSerializer, CarCategorySerializer

class CarListView(generics.ListAPIView):
    serializer_class = CarSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['category__slug', 'make', 'year']
    ordering_fields = ['daily_rate', 'year', 'make', 'created_at']
    ordering = ['-created_at']
    search_fields = [
        'make',                        # brand like "Toyota"
        'model',                       # model like "Corolla"
        'description',                 # text description
        'additional_km_rate',          # text field e.g., "AED 5 – AED 30"
        'seats',                       # number of seats
        'doors',                       # number of doors
        'passengers',                  # number of passengers
        'luggage_capacity',            # number of luggage bags
        'security_deposit',            # amount as text
        'category__name',              # car category name
        'category__slug',              # car category slug
    ]

    def get_queryset(self):
        return Car.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class CarDetailView(generics.RetrieveAPIView):
    serializer_class = CarSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'
    queryset = Car.objects.all()

class CarCategoryListView(generics.ListAPIView):
    serializer_class = CarCategorySerializer
    permission_classes = [AllowAny]
    queryset = CarCategory.objects.all()

class LocationListView(generics.ListAPIView):
    serializer_class = LocationSerializer
    permission_classes = [AllowAny]
    queryset = Location.objects.all()

class FAQListView(generics.ListAPIView):
    serializer_class = FAQSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['category__slug']  # Filter by category slug
    ordering_fields = ['order', 'question']
    ordering = ['order']
    
    def get_queryset(self):
        queryset = FAQ.objects.all()
        # Optional: Filter by search query
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(
                models.Q(question__icontains=search_query) |
                models.Q(answer__icontains=search_query)
            )
        return queryset

class ContentSectionListView(generics.ListAPIView):
    serializer_class = ContentSectionSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['page']
    
    def get_queryset(self):
        queryset = ContentSection.objects.all()
        return queryset
    
def create_admin(request):
    if not User.objects.filter(username='seud').exists():
        User.objects.create_superuser('seud', 'seudsahm1@gmail.com', '12345678')
        return HttpResponse("Admin user created")
    return HttpResponse("Admin user already exists")

class CustomerReviewListView(generics.ListAPIView):
    queryset = CustomerReview.objects.all()
    serializer_class = CustomerReviewSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['slug']
    
class SiteInfoListView(generics.ListAPIView):
    queryset = SiteInfo.objects.all()
    serializer_class = SiteInfoSerializer
    permission_classes = [AllowAny]
    
class AdUnitListView(generics.ListAPIView):
    queryset = AdUnit.objects.filter(is_active=True)
    serializer_class = AdUnitSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['page', 'slug']
    
def ads_txt_view(request):
    publisher_id = settings.GOOGLE_ADSENSE_PUBLISHER_ID
    if not publisher_id:
        return HttpResponse("Publisher ID not configured", status=500)
    content = f"google.com, {publisher_id}, DIRECT, f08c47fec0942fa0"
    return HttpResponse(content, content_type='text/plain')