from django.db import models

# This model defines the structure for a learning topic.
class Topic(models.Model):
    title = models.CharField(max_length=200)
    grade_level = models.CharField(max_length=50)
    subject = models.CharField(max_length=50)
    content_body = models.TextField()
    badge_name = models.CharField(max_length=100, default="Knowledge Seeker")

    def __str__(self):
        # This makes the admin panel more readable.
        return self.title

# This model defines the structure for a quiz question.
class QuizQuestion(models.Model):
    # This links each question to a specific Topic.
    # If a Topic is deleted, all its questions are also deleted.
    topic = models.ForeignKey(Topic, related_name='questions', on_delete=models.CASCADE)
    question_text = models.CharField(max_length=255)
    # We'll store choices as text separated by a pipe '|', e.g., "Choice A|Choice B|Choice C"
    choices = models.CharField(max_length=255) 
    # The correct choice will be stored as a number (0 for the first choice, 1 for the second, etc.)
    correct_choice = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.question_text