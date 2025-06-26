from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import HomepageHero, FAQ, BlogPost, Testimonial, AdPlacement
from .serializers import (
    HomepageHeroSerializer, FAQSerializer, BlogPostSerializer,
    TestimonialSerializer, AdPlacementSerializer
)

class HomepageHeroListView(generics.ListAPIView):
    queryset = HomepageHero.objects.filter(is_active=True)
    serializer_class = HomepageHeroSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['order']

class FAQListView(generics.ListAPIView):
    queryset = FAQ.objects.filter(is_active=True)
    serializer_class = FAQSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category']
    search_fields = ['question', 'answer']

class BlogPostListView(generics.ListAPIView):
    queryset = BlogPost.objects.filter(is_active=True)
    serializer_class = BlogPostSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category']
    search_fields = ['title', 'content']

class BlogPostDetailView(generics.RetrieveAPIView):
    queryset = BlogPost.objects.filter(is_active=True)
    serializer_class = BlogPostSerializer
    lookup_field = 'slug'

class TestimonialListView(generics.ListAPIView):
    queryset = Testimonial.objects.filter(is_featured=True)
    serializer_class = TestimonialSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['rating']

class AdPlacementListView(generics.ListAPIView):
    queryset = AdPlacement.objects.filter(is_active=True)
    serializer_class = AdPlacementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['page']