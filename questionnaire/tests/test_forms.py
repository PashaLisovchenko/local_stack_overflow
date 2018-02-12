from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.utils.text import slugify
from markdownx.fields import MarkdownxFormField
from questionnaire.forms import AddQuestion, AnswerForm, CommentForm
from django.urls import reverse
from questionnaire.models import Question, Answer
from questionnaire.views import AddQuestionView, CommentAddQuestion, CommentAddAnswer


class AddQuestionFormTest(TestCase):

    def test_text_question_it_is_markdown_field(self):
        form = AddQuestion()
        self.assertTrue(isinstance(form.fields['text_question'], MarkdownxFormField))

    def test_add_question_view_post_valid(self):
        user = User.objects.create_user(username='testuser4', password='123123')
        url = reverse('question:add_question')
        data = {
            'title': 'question-1',
            'text_question': 'question_text_1',
            'tags': 'django, python',
        }
        form = AddQuestion(data=data)
        self.assertTrue(form.is_valid())
        rf = RequestFactory()
        request = rf.post(url, data)
        request.user = user
        response = AddQuestionView.as_view()(request)
        self.assertEqual(response.status_code, 302)


class AnswerFormTest(TestCase):

    def test_text_question_it_is_markdown_field(self):
        form = AnswerForm()
        self.assertTrue(isinstance(form.fields['text_answer'], MarkdownxFormField))


class CommentFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='testuser5', password='123123')
        user.save()
        user1 = User.objects.create_user(username='testuser6', password='123123')
        user1.save()
        slug = slugify('q-11')
        question = Question.objects.create(id=11, title='q-11', text_question='q-text-11', user=user, slug=slug)
        Answer.objects.create(id=11, text_answer='answer-1', question=question, user=user1)

    def test_add_comment_question(self):
        question = Question.objects.get(id=11)
        kwargs = {'id': question.id}
        url = reverse('question:comment-add-question', kwargs=kwargs)
        data = {
            'comment': 'comment_question_1',
        }
        form = CommentForm(data=data)
        self.assertTrue(form.is_valid())
        rf = RequestFactory()
        request = rf.post(url, data)
        request.user = question.user
        kwargs = {'id': question.id, 'slug': question.slug}
        response = CommentAddQuestion.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 302)

    def test_add_comment_answer(self):
        answer = Answer.objects.get(id=11)
        kwargs = {'id': answer.id}
        url = reverse('question:comment-add-answer', kwargs=kwargs)
        data = {
            'comment': 'comment_answer_1',
        }
        form = CommentForm(data=data)
        self.assertTrue(form.is_valid())
        rf = RequestFactory()
        request = rf.post(url, data)
        request.user = answer.user
        kwargs = {'id': answer.question.id, 'slug': answer.question.slug}
        response = CommentAddAnswer.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 302)