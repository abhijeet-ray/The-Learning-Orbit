from django.contrib import admin
from .models import Topic, QuizQuestion # Import our models

# This line tells the admin panel to create an interface for the Topic model.
admin.site.register(Topic)

# This line does the same for the QuizQuestion model.
admin.site.register(QuizQuestion)