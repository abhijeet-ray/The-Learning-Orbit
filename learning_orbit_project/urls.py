# learning_orbit_project/urls.py

from django.contrib import admin
from django.urls import path, include
from topics import views as topics_views
# NEW: Import settings and static for file serving
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('topics/', include('topics.urls')),
    path('', topics_views.homepage_view, name='homepage'), 
]

# NEW: This line is added to serve media files during development.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)