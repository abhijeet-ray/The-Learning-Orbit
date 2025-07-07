# topics/urls.py
from django.urls import path
from . import views # We will create this view function next

urlpatterns = [
    # This creates a URL like /topics/1/, /topics/2/, etc.
    # The <int:topic_id> part captures the number from the URL.
    path('<int:topic_id>/', views.topic_detail_view, name='topic_detail'),
]