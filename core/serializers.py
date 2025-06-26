from rest_framework import serializers
from .models import SiteConfiguration, SocialMediaLink, PageMeta, Language, Translation

class SiteConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteConfiguration
        fields = [
            'google_adsense_client_id',
            'google_maps_api_key',
            'whatsapp_default_message'
        ]

class SocialMediaLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaLink
        fields = ['platform', 'url', 'icon_class', 'is_active', 'order']

class PageMetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageMeta
        fields = ['page', 'title', 'description', 'keywords', 'canonical_url']

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['code', 'name', 'is_active', 'is_default']

class TranslationSerializer(serializers.ModelSerializer):
    language = LanguageSerializer(read_only=True)

    class Meta:
        model = Translation
        fields = ['key', 'language', 'value']