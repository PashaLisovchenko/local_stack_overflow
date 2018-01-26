from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Question
from taggit.models import Tag


class QuestionList(ListView):
    template_name = 'questionnaire/question_list.html'
    model = Question
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super(QuestionList, self).get_context_data(**kwargs)
        context['section'] = 'Question'
        return context


class TagList(ListView):
    template_name = 'questionnaire/tag_list.html'
    model = Tag
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super(TagList, self).get_context_data(**kwargs)
        context['section'] = 'Tags'
        return context


class UserList(ListView):
    template_name = 'questionnaire/user_list.html'
    model = User
    paginate_by = 45

    def get_context_data(self, **kwargs):
        context = super(UserList, self).get_context_data(**kwargs)

        # names = Tag.objects.values_list('name', flat=True)
        # print(names)
        # user = User.objects.get(username='pasha')
        # questions = user.questions.all()
        # question_user = [q for q in questions]
        # tags_user = [t.tags.all() for t in question_user]
        # print(tags_user)

        # t = [t for t in tags_user]
        # print(t)
        # tag = [for t in tags_user]
        # print(tag)

        # documents = list(Document.objects.filter(name__in=names))
        context['section'] = 'Users'
        return context


class QuestionListByTag(DetailView):
    template_name = 'questionnaire/tag_detail.html'
    model = Tag
    slug_url_kwarg = 'tag_slug'

    def get_context_data(self, **kwargs):
        context = super(QuestionListByTag, self).get_context_data(**kwargs)
        questions = Question.objects.filter(tags__name__in=[self.object.name])
        context['questions'] = questions
        context['section'] = 'Question'
        return context
