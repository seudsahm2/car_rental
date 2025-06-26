from django.urls import path  
from .views import (  
    HomepageHeroListView,  
    FAQListView,  
    BlogPostListView,  
    BlogPostDetailView,  
    TestimonialListView,  
    AdPlacementListView,  
)  

urlpatterns = [
    path('homepage-hero/', HomepageHeroListView.as_view(), name='homepage-hero-list'),
    path('faqs/', FAQListView.as_view(), name='faq-list'),
    path('blog/', BlogPostListView.as_view(), name='blog-list'),
    path('blog/<slug:slug>/', BlogPostDetailView.as_view(), name='blog-detail'),
    path('testimonials/', TestimonialListView.as_view(), name='testimonial-list'),
    path('ads/', AdPlacementListView.as_view(), name='ad-placement-list'),
]