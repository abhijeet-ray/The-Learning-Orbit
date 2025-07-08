# topics/models.py
from django.db import models

class Topic(models.Model):
    # These fields remain as they describe the topic itself.
    title = models.CharField(max_length=200)
    grade_level = models.CharField(max_length=50)
    subject = models.CharField(max_length=50)
    badge_name = models.CharField(max_length=100, default="Knowledge Seeker")
    is_featured = models.BooleanField(default=False)
    
    # We are removing content_body, image_url, and reverse_engineer_challenge.
    # They will now be handled by ContentBlocks.

    def __str__(self):
        return self.title

# NEW: This is our flexible content block model.
class ContentBlock(models.Model):
    # Each block belongs to a single topic.
    topic = models.ForeignKey(Topic, related_name='content_blocks', on_delete=models.CASCADE)

    # Define the types of blocks we can have.
    BLOCK_TYPES = [
        ('heading', 'Heading'),
        ('paragraph', 'Paragraph'),
        ('image', 'Image'),
        ('sandbox_greenhouse', 'Sandbox: Virtual Greenhouse'),
        ('quiz', 'Quiz'),
        ('challenge', 'Reverse-Engineer Challenge'),
    ]
    block_type = models.CharField(max_length=20, choices=BLOCK_TYPES)

    # A field to control the order of the blocks on the page.
    order = models.PositiveIntegerField(default=0)

    # Fields to store the content for each block type.
    # Most will be optional (blank=True, null=True).
    text_content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='topic_images/', blank=True, null=True)

    # This helps order the blocks correctly in the admin panel and on the page.
    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.topic.title} - Block {self.order} ({self.get_block_type_display()})"


# The QuizQuestion model remains, as it's a distinct part of the Quiz block.
class QuizQuestion(models.Model):
    topic = models.ForeignKey(Topic, related_name='questions', on_delete=models.CASCADE)
    question_text = models.CharField(max_length=255)
    choices = models.CharField(max_length=255) 
    correct_choice = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.question_text