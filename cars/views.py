# cars/views.py

from rest_framework import generics, filters
from .models import Car, CarCategory,FAQ,ContentSection,CustomerReview,SiteInfo,AdUnit
from .serializers import CarSerializer, CarCategorySerializer, FAQSerializer, ContentSectionSerializer,CustomerReviewSerializer,SiteInfoSerializer,AdUnitSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from django.http import HttpResponse
from django.contrib.auth.models import User
from .utils.supabase_client import get_supabase_client
# Views
class CarListView(generics.ListAPIView):
    serializer_class = CarSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['category__slug', 'make', 'year']
    ordering_fields = ['daily_rate', 'year', 'make', 'created_at']
    ordering = ['-created_at']
    search_fields = ['make', 'model', 'description']

    def get_queryset(self):
        supabase = get_supabase_client()
        response = supabase.table('cars').select('*').execute()
        return response.data  # Return Supabase data as queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class CarCategoryListView(generics.ListAPIView):
    queryset = CarCategory.objects.all()
    serializer_class = CarCategorySerializer
    permission_classes = [AllowAny]

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