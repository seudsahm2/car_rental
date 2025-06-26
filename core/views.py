from rest_framework import generics
from .models import SiteConfiguration, SocialMediaLink, PageMeta, Language, Translation
from .serializers import (
    SiteConfigurationSerializer,
    SocialMediaLinkSerializer,
    PageMetaSerializer,
    LanguageSerializer,
    TranslationSerializer
)

class SiteConfigurationView(generics.RetrieveAPIView):
    queryset = SiteConfiguration.objects.all()
    serializer_class = SiteConfigurationSerializer

    def get_object(self):
        return SiteConfiguration.objects.first()  # Singleton pattern

class SocialMediaLinkListView(generics.ListAPIView):
    queryset = SocialMediaLink.objects.filter(is_active=True)
    serializer_class = SocialMediaLinkSerializer
    filter_fields = ['platform']

class PageMetaListView(generics.ListAPIView):
    queryset = PageMeta.objects.all()
    serializer_class = PageMetaSerializer
    search_fields = ['page', 'title']

class PageMetaDetailView(generics.RetrieveAPIView):
    queryset = PageMeta.objects.all()
    serializer_class = PageMetaSerializer
    lookup_field = 'page'

class LanguageListView(generics.ListAPIView):
    queryset = Language.objects.filter(is_active=True)
    serializer_class = LanguageSerializer

class TranslationListView(generics.ListAPIView):
    queryset = Translation.objects.all()
    serializer_class = TranslationSerializer
    filter_fields = ['language']
    search_fields = ['key']