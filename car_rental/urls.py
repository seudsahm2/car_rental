import os
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('cars.urls')),
    path('api/', include('fleet.urls')),
    path('api/', include('locations.urls')),
    path('api/', include('content.urls')),
    path('api/', include('core.urls')),
    path('api/', include('deals.urls')),
    path('api/', include('people.urls')),
    path('api/', include('sales.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
# Serve media files locally in development
if settings.DEBUG and not os.getenv('REMOTE_DB', 'False').lower() in ('true', '1', 'yes'):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)