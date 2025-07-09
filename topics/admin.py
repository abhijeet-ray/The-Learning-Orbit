# topics/admin.py

from django.contrib import admin
from .models import Topic, QuizQuestion

# This customizes how the main Topic admin page looks.
class TopicAdmin(admin.ModelAdmin):
    # These are the columns that will be displayed in the topic list
    list_display = ('title', 'subject', 'grade_level', 'is_featured')
    # This adds a filter sidebar
    list_filter = ('subject', 'grade_level', 'is_featured')
    # This adds a search bar to search these fields
    search_fields = ('title', 'content_html')

# Register our models with the admin site.
admin.site.register(Topic, TopicAdmin)
admin.site.register(QuizQuestion)