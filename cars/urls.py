from django.urls import path
from .views import CarListView, CarCategoryListView, FAQListView,ContentSectionListView

urlpatterns = [
    path('cars/', CarListView.as_view(), name='car-list'),
    path('categories/', CarCategoryListView.as_view(), name='category-list'),
    path('faqs/', FAQListView.as_view(), name='faq-list'),
    path('content-sections/', ContentSectionListView.as_view(), name='content-section-list'),
]