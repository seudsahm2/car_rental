from django.urls import path
from .views import (
    LocationListView,
    LocationDetailView,
    LocationSpecificDealListView,
    LocationSpecificDealDetailView,
)

urlpatterns = [
    path('locations/', LocationListView.as_view(), name='location-list'),
    path('locations/<slug:slug>/', LocationDetailView.as_view(), name='location-detail'),
    path('deals/', LocationSpecificDealListView.as_view(), name='deal-list'),
    path('deals/<slug:slug>/', LocationSpecificDealDetailView.as_view(), name='deal-detail'),
]