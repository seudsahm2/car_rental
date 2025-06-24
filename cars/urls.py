from django.urls import path
from .views import CarListView, CarCategoryListView, FAQListView,ContentSectionListView,create_admin,CustomerReviewListView,SiteInfoListView

urlpatterns = [
    path('cars/', CarListView.as_view(), name='car-list'),
    path('categories/', CarCategoryListView.as_view(), name='category-list'),
    path('faqs/', FAQListView.as_view(), name='faq-list'),
    path('content-sections/', ContentSectionListView.as_view(), name='content-section-list'),
    path("create/",create_admin, name="create_admin"),
    path('customer-reviews/', CustomerReviewListView.as_view(), name='customer-review-list'),
    path('site-info/', SiteInfoListView.as_view(), name='site-info-list'),
]