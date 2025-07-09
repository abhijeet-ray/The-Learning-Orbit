# topics/models.py
from django.db import models

class Topic(models.Model):
    title = models.CharField(max_length=200)
    grade_level = models.CharField(max_length=50)
    subject = models.CharField(max_length=50)
    badge_name = models.CharField(max_length=100, default="Knowledge Seeker")
    is_featured = models.BooleanField(default=False)
    
    # The new, single field for all our rich content.
    content_html = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

# The QuizQuestion model is now linked directly to the Topic.
class QuizQuestion(models.Model):
    topic = models.ForeignKey(Topic, related_name='questions', on_delete=models.CASCADE)
    question_text = models.CharField(max_length=255)
    choices = models.CharField(max_length=255) 
    correct_choice = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.question_text