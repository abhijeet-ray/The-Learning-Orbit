# learning_orbit_project/urls.py
from django.contrib import admin
from django.urls import path, include
from topics import views as topics_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('topics/', include('topics.urls')),
    
    # NEW: URL for the list of topics for a specific subject within a grade
    path('k-12/<slug:grade_slug>/<slug:subject_slug>/', topics_views.subject_topics_view, name='subject_topics'),
    
    # This URL now shows the list of subjects for a grade
    path('k-12/<slug:grade_slug>/', topics_views.grade_subjects_view, name='grade_subjects'),
    
    path('k-12/', topics_views.k12_galaxy_view, name='k12_galaxy'),
    path('', topics_views.homepage_view, name='homepage'), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)