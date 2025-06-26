from django.urls import path
from .views import TeamMemberListView, NewsletterSubscriberListView

urlpatterns = [
    path('team/', TeamMemberListView.as_view(), name='team-list'),
    path('subscribers/', NewsletterSubscriberListView.as_view(), name='subscriber-list'),
]