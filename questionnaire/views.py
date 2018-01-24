from django.db.models import F, DateTimeField, ExpressionWrapper
from django.shortcuts import render
from django.views.generic import ListView
from .models import Question
import datetime


class QuestionList(ListView):
    template_name = 'templates/question_list.html'
    model = Question

    # def get_context_data(self, **kwargs):
    #     context = super(QuestionList, self).get_context_data(**kwargs)
    #     return context
