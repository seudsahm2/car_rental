from rest_framework import generics
from .models import TeamMember, NewsletterSubscriber
from .serializers import TeamMemberSerializer, NewsletterSubscriberSerializer

class TeamMemberListView(generics.ListAPIView):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
    ordering_fields = ['order']

class NewsletterSubscriberListView(generics.ListAPIView):
    queryset = NewsletterSubscriber.objects.filter(is_active=True)
    serializer_class = NewsletterSubscriberSerializer
    ordering_fields = ['-subscribed_at']
    search_fields = ['email']