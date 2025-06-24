# cars/views.py

from rest_framework import generics, filters
from .models import Car, CarCategory,FAQ,ContentSection
from .serializers import CarSerializer, CarCategorySerializer, FAQSerializer, ContentSectionSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from django.http import HttpResponse
from django.contrib.auth.models import User
# Views
class CarListView(generics.ListAPIView):
    serializer_class = CarSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['category__slug', 'make', 'year']  # Enhanced filtering
    ordering_fields = ['daily_rate', 'year', 'make', 'created_at']
    ordering = ['-created_at']
    search_fields = ['make', 'model', 'description']  # Added search fields
    
    def get_queryset(self):
        queryset = Car.objects.all()
        return queryset
    
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
