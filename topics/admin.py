# topics/admin.py

from django.contrib import admin
from .models import Topic, ContentBlock, QuizQuestion

# This allows us to edit ContentBlocks directly on the Topic page.
class ContentBlockInline(admin.TabularInline):
    model = ContentBlock
    extra = 1 # Show one extra empty block to add to.
    # This allows you to reorder the blocks by dragging them.
    ordering = ('order',)

# This customizes how the main Topic admin page looks.
class TopicAdmin(admin.ModelAdmin):
    # This includes the ContentBlock editor on the Topic page.
    inlines = [ContentBlockInline]
    list_display = ('title', 'subject', 'grade_level', 'is_featured')
    list_filter = ('subject', 'grade_level', 'is_featured')

# We are now just registering our new TopicAdmin directly.
admin.site.register(Topic, TopicAdmin)

# We still need a separate page for managing quiz questions.
admin.site.register(QuizQuestion)