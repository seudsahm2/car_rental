from django.urls import path
from .views import (
    SiteConfigurationView,
    SocialMediaLinkListView,
    PageMetaListView,
    PageMetaDetailView,
    LanguageListView,
    TranslationListView,
)

urlpatterns = [
    path('site-config/', SiteConfigurationView.as_view(), name='site-config'),
    path('social-links/', SocialMediaLinkListView.as_view(), name='social-links'),
    path('page-meta/', PageMetaListView.as_view(), name='page-meta-list'),
    path('page-meta/<str:page>/', PageMetaDetailView.as_view(), name='page-meta-detail'),
    path('languages/', LanguageListView.as_view(), name='language-list'),
    path('translations/', TranslationListView.as_view(), name='translation-list'),
]