from django import template
from django.db.models import Count
from taggit.models import Tag

from ..models import Question

register = template.Library()


@register.simple_tag
def total_question():
    return Question.objects.all().count()


@register.inclusion_tag('questionnaire/latest_question.html')
def show_latest_question(count=5):
    latest_questions = Question.objects.all().order_by('-created')[:count]
    return {'latest_question': latest_questions}


@register.assignment_tag
def get_most_answer_question(count=5):
    return Question.objects.all().annotate(
        total_answer=Count('answers')
    ).order_by('-total_answer')[:count]


@register.assignment_tag
def get_most_taggit(count=5):
    return Tag.objects.all().annotate(
        total_use=Count('taggit_taggeditem_items')
    ).order_by('-total_use')[:count]