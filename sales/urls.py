from django.urls import path
from .views import BookingRequestListView, ContactInquiryListView

urlpatterns = [
    path('booking-requests/', BookingRequestListView.as_view(), name='booking-request-list'),
    path('contact-inquiries/', ContactInquiryListView.as_view(), name='contact-inquiry-list'),
]