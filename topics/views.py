# topics/views.py
from django.shortcuts import render, get_object_or_404
from django.db import models
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Topic

def topic_detail_view(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    # THIS IS THE CRUCIAL LINE: Get all content blocks for this topic.
    content_blocks = topic.content_blocks.all()
    
    context = {
        'topic': topic,
        # THIS IS THE FIX: Add the content blocks to the context.
        'content_blocks': content_blocks,
    }

    if request.method == 'POST':
        if 'submit_quiz' in request.POST:
            score = 0
            quiz_questions = topic.questions.all()
            total_questions = len(quiz_questions)
            for question in quiz_questions:
                input_name = f'question_{question.id}'
                user_answer = request.POST.get(input_name)
                if user_answer is not None and int(user_answer) == question.correct_choice:
                    score += 1
            request.session['quiz_results'] = {'score': score, 'total': total_questions}
            return HttpResponseRedirect(reverse('topic_detail', args=[topic_id]) + '#quiz-results-anchor')

        if 'submit_challenge' in request.POST:
            user_challenge_answer = request.POST.get('challenge_answer', '')
            if 'cycle' in user_challenge_answer.lower() and 'oxygen' in user_challenge_answer.lower() and 'carbon' in user_challenge_answer.lower():
                challenge_feedback = "Excellent! You correctly identified the gas cycle."
                challenge_success = True
            else:
                challenge_feedback = "Good start, but try to be more specific about the gas cycle."
                challenge_success = False
            request.session['challenge_results'] = {'feedback': challenge_feedback, 'success': challenge_success}
            return HttpResponseRedirect(reverse('topic_detail', args=[topic_id]) + '#challenge-results-anchor')

    if 'quiz_results' in request.session:
        results = request.session.pop('quiz_results')
        context.update({'quiz_results': True, 'score': results['score'], 'total_questions': results['total']})

    if 'challenge_results' in request.session:
        results = request.session.pop('challenge_results')
        context.update({'challenge_results': True, 'challenge_feedback': results['feedback'], 'challenge_success': results['success']})

    quiz_questions = topic.questions.all()
    for question in quiz_questions:
        question.choices_list = question.choices.split('|')
    context['quiz_questions'] = quiz_questions
    
    recently_viewed_ids = request.session.get('recently_viewed', [])
    if topic_id in recently_viewed_ids:
        recently_viewed_ids.remove(topic_id)
    recently_viewed_ids.insert(0, topic_id)
    request.session['recently_viewed'] = recently_viewed_ids[:5]

    return render(request, 'topics/topic_detail.html', context)


def homepage_view(request):
    featured_topics = Topic.objects.filter(is_featured=True)
    other_topics = Topic.objects.filter(is_featured=False)
    recently_viewed_ids = request.session.get('recently_viewed', [])
    recent_topics = []
    if recently_viewed_ids:
        preserved_order = models.Case(*[models.When(pk=pk, then=pos) for pos, pk in enumerate(recently_viewed_ids)])
        recent_topics = Topic.objects.filter(pk__in=recently_viewed_ids).order_by(preserved_order)

    context = {
        'featured_topics': featured_topics,
        'other_topics': other_topics,
        'recent_topics': recent_topics,
    }
    return render(request, 'topics/homepage.html', context)