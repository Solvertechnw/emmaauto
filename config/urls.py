from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static  # <-- add this import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cars.urls')),  # Include app URLs properly
]

# ✅ This serves uploaded images in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
