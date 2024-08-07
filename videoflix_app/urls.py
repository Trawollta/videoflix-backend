from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('user.urls')),
    path('videos/', include('streaming.urls')),  # Hier den richtigen Namen verwenden
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)