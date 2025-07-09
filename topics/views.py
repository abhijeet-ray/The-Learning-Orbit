# topics/views.py
from django.shortcuts import render, get_object_or_404
from django.db import models
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Topic

def topic_detail_view(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    quiz_questions = topic.questions.all()

    # Prepare the choices for the quiz questions
    for question in quiz_questions:
        question.choices_list = question.choices.split('|')

    # Start with our essential context
    context = {
        'topic': topic,
        'quiz_questions': quiz_questions,
    }

    # Handle a POST request (form submission)
    if request.method == 'POST':
        if 'submit_quiz' in request.POST:
            score = 0
            total_questions = len(quiz_questions)
            for question in quiz_questions:
                user_answer = request.POST.get(f'question_{question.id}')
                if user_answer is not None and int(user_answer) == question.correct_choice:
                    score += 1
            # Store results in the session so they persist after redirect
            request.session['quiz_results'] = {'score': score, 'total': total_questions}
            # Redirect to the same page with an anchor
            return HttpResponseRedirect(reverse('topic_detail', args=[topic_id]) + '#quiz-results-anchor')

    # Handle displaying results from the session after a redirect
    if 'quiz_results' in request.session:
        # Use .pop() to get the results and remove them from the session
        results = request.session.pop('quiz_results') 
        context.update({
            'quiz_results_visible': True, 
            'score': results['score'], 
            'total': results['total']
        })
        
    # Handle recently viewed topics
    recently_viewed_ids = request.session.get('recently_viewed', [])
    if topic_id in recently_viewed_ids:
        recently_viewed_ids.remove(topic_id)
    recently_viewed_ids.insert(0, topic_id)
    request.session['recently_viewed'] = recently_viewed_ids[:5]

    return render(request, 'topics/topic_detail.html', context)


# --- HOMEPAGE AND K-12 VIEWS (These are already correct, but included for completeness) ---
def homepage_view(request):
    # This view is correct and does not need changes.
    featured_topics = Topic.objects.filter(is_featured=True)
    other_topics = Topic.objects.filter(is_featured=False)
    recently_viewed_ids = request.session.get('recently_viewed', [])
    recent_topics = []
    if recently_viewed_ids:
        preserved_order = models.Case(*[models.When(pk=pk, then=pos) for pos, pk in enumerate(recently_viewed_ids)])
        recent_topics = Topic.objects.filter(pk__in=recently_viewed_ids).order_by(preserved_order)
    context = {'featured_topics': featured_topics, 'other_topics': other_topics, 'recent_topics': recent_topics}
    return render(request, 'topics/homepage.html', context)

def k12_galaxy_view(request):
    grade_levels_qs = Topic.objects.values_list('grade_level', flat=True).distinct().order_by('grade_level')
    context = { 'grade_levels': list(grade_levels_qs) }
    return render(request, 'topics/k12_landing.html', context)

def grade_subjects_view(request, grade_slug):
    grade_name = grade_slug.replace('-', ' ').title()
    subjects_qs = Topic.objects.filter(grade_level=grade_name).values_list('subject', flat=True).distinct().order_by('subject')
    context = {'grade_name': grade_name, 'grade_slug': grade_slug, 'subjects_list': list(subjects_qs)}
    return render(request, 'topics/grade_subjects_list.html', context)

def subject_topics_view(request, grade_slug, subject_slug):
    grade_name = grade_slug.replace('-', ' ').title()
    subject_name = subject_slug.replace('-', ' ').title()
    topics = Topic.objects.filter(grade_level=grade_name, subject=subject_name)
    context = {'grade_name': grade_name, 'subject_name': subject_name, 'topics_list': topics}
    return render(request, 'topics/subject_topics_list.html', context)