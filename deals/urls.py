from django.urls import path
from .views import (
    MonthlyRentalDealListView,
    PromoBannerListView,
    ServiceBenefitListView
)

urlpatterns = [
    path('monthly-deals/', MonthlyRentalDealListView.as_view(), name='monthly-deals'),
    path('promo-banners/', PromoBannerListView.as_view(), name='promo-banners'),
    path('service-benefits/', ServiceBenefitListView.as_view(), name='service-benefits'),
]