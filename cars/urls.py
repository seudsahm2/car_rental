from django.urls import path
from django.http import HttpResponse
from django.conf import settings
from .views import CarCategoryListView, CarListView, FAQListView, ContentSectionListView, CustomerReviewListView, SiteInfoListView, AdUnitListView,create_admin,ads_txt_view



urlpatterns = [
    path('cars/', CarListView.as_view(), name='car-list'),
    path('categories/', CarCategoryListView.as_view(), name='category-list'),
    path('faqs/', FAQListView.as_view(), name='faq-list'),
    path('content-sections/', ContentSectionListView.as_view(), name='content-section-list'),
    path("create/",create_admin, name="create_admin"),
    path('customer-reviews/', CustomerReviewListView.as_view(), name='customer-review-list'),
    path('site-info/', SiteInfoListView.as_view(), name='site-info-list'),
    path('ad-units/', AdUnitListView.as_view(), name='ad-unit-list'),
    path('ads.txt', ads_txt_view, name='ads-txt'),
]