from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin, FormView, CreateView
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from questionnaire.forms import AnswerForm, CommentForm, AddQuestion
from .models import Question, Answer, Comment
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
    paginate_by = 36

    def get_context_data(self, **kwargs):
        context = super(UserList, self).get_context_data(**kwargs)
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


class QuestionDetail(FormMixin, DetailView):
    template_name = 'questionnaire/question_detail.html'
    model = Question
    form_class = AnswerForm
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super(QuestionDetail, self).get_context_data(**kwargs)
        context['section'] = 'Question'
        form_comment = CommentForm()
        context['form_comment'] = form_comment

        question = self.object

        content_type = ContentType.objects.get_for_model(question)
        question_comment_list = Comment.objects.filter(
            content_type__pk=content_type.pk,
            object_id=question.pk
        )
        answers = question.answers.all()
        answers_id = [a.id for a in answers]

        content_type = ContentType.objects.get_for_model(Answer)
        answers_comment_list = Comment.objects.filter(
            content_type__pk=content_type.pk,
            object_id__in=answers_id
        )
        question_tags_ids = question.tags.values_list('id', flat=True)
        similar_question = Question.objects.filter(tags__in=question_tags_ids).exclude(id=question.id)
        similar_question = similar_question.annotate(same_tags=Count('tags')).order_by('-same_tags')[:5]
        context['similar_question'] = similar_question
        context['question_comment_list'] = question_comment_list
        context['answers_comment_list'] = answers_comment_list
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        object = self.get_object()
        user = self.request.user
        text_answer = self.request.POST.get("text_answer")
        Answer.objects.create(user=user, question=object, text_answer=text_answer)
        return redirect(object)


class CommentAddAnswer(DetailView, FormMixin):
    form_class = CommentForm
    model = Answer
    pk_url_kwarg = "id"

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        object = self.get_object()
        user = self.request.user
        text_comment = self.request.POST.get('comment')
        content_type = ContentType.objects.get_for_model(object)
        print(content_type)
        new_comment = Comment.objects.create(
            content_type=content_type,
            object_id=object.pk,
            user=user,
            comment=text_comment
        )
        new_comment.save()
        return redirect(object.question)


class CommentAddQuestion(DetailView, FormMixin):
    form_class = CommentForm
    model = Question
    pk_url_kwarg = "id"

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        object = self.get_object()
        user = self.request.user
        text_comment = self.request.POST.get('comment')
        content_type = ContentType.objects.get_for_model(object)
        print(content_type)
        new_comment = Comment.objects.create(
            content_type=content_type,
            object_id=object.pk,
            user=user,
            comment=text_comment
        )
        new_comment.save()
        return redirect(object)


class AddQuestionView(CreateView):
    template_name = 'questionnaire/add_question.html'
    form_class = AddQuestion
    model = Question

    def form_valid(self, form):
        cl = form.cleaned_data
        tags = cl['tags']
        slug = slugify(cl['title'])
        user = self.request.user
        question = Question(user=user, slug=slug, title=cl['title'], text_question=cl['text_question'])
        question.save()
        for tag in tags:
            question.tags.add(tag)
        return redirect(reverse_lazy('question:question_detail', kwargs={'id':question.id, 'slug': question.slug}))


def current_answer(request):
    answer = request.GET.get('answer_id', None)
    correct = request.GET.get('correct', None)
    answer = Answer.objects.get(id=answer)
    if correct == 'true':
        answer.is_correct = True
    elif correct == 'false':
        answer.is_correct = False
    answer.save()
    data = {
        'is_correct': answer.is_correct
    }
    return JsonResponse(data)


@login_required
@require_POST
def user_like(request):
    model_name = request.POST.get('model_name')
    id = request.POST.get('id')
    action = request.POST.get('action')
    if id and action:
        try:
            if model_name == 'question':
                question = Question.objects.get(id=id)
                if action == 'like':
                    question.users_like.add(request.user)
                else:
                    question.users_like.remove(request.user)
            else:
                answer = Answer.objects.get(id=id)
                if action == 'like':
                    answer.users_like.add(request.user)
                else:
                    answer.users_like.remove(request.user)
            return JsonResponse({'status': 'ok', 'id': id})
        except:
            pass
            return JsonResponse({'status': 'ko'})
