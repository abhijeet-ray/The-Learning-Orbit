# topics/views.py
from django.shortcuts import render, get_object_or_404
from .models import Topic

def topic_detail_view(request, topic_id):
    # Fetch the topic from the database using the id from the URL.
    # If no topic with that id is found, it will show a 404 Not Found page.
    topic = get_object_or_404(Topic, pk=topic_id)

    # We create a 'context' dictionary to pass data to our template.
    context = {
        'topic': topic
    }

    # Render the HTML template, passing in the context data.
    return render(request, 'topics/topic_detail.html', context)