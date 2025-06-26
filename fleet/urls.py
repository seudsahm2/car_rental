from django.urls import path
from .views import CarListView, CarDetailView, CarCategoryListView

urlpatterns = [
    path('carss/', CarListView.as_view(), name='car-list'),
    path('carss/<slug:slug>/', CarDetailView.as_view(), name='car-detail'),
    path('categoriess/', CarCategoryListView.as_view(), name='category-list'),
]