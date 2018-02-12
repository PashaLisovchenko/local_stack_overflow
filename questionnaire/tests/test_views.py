from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.utils.text import slugify
from taggit.models import Tag
from questionnaire.models import Question, Answer
from questionnaire.views import QuestionListByTag


class QuestionListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create 18 question for pagination tests
        user = User.objects.create(username='pasha', password='12345')
        number_of_question = 18
        for question_num in range(number_of_question):
            slug = slugify('Question %s' % question_num)
            Question.objects.create(title='Question %s' % question_num, text_question='text %s' % question_num,
                                    user=user, slug=slug)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('question:home_page'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('question:home_page'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'questionnaire/question_list.html')

    def test_pagination_is_fifteen(self):
        resp = self.client.get(reverse('question:home_page'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] is True)
        self.assertTrue(len(resp.context['question_list']) == 15)

    def test_lists_all_question(self):
        resp = self.client.get(reverse('question:home_page') + '?page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] is True)
        self.assertTrue(len(resp.context['question_list']) == 3)


class QuestionListByTagTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Tag.objects.create(name='html')
        user = User.objects.create(username='pasha', password='12345')
        number_of_question = 5
        for question_num in range(number_of_question):
            slug = slugify('Question %s' % question_num)
            q = Question.objects.create(title='Question %s' % question_num, text_question='text %s' % question_num,
                                        user=user, slug=slug)
            if question_num % 2 == 0:
                q.tags.add('html')

    def test_question_by_tag_get_context(self):
        tag = Tag.objects.get(name='html')
        kwargs = {'tag_slug': tag.slug}
        url = reverse("question:tag_detail", kwargs=kwargs)
        factory = RequestFactory()
        request = factory.get(url)
        response = QuestionListByTag.as_view()(request, **kwargs)
        questions = Question.objects.filter(tags__name__in=[tag.name])
        self.assertEqual(response.status_code, 200)
        for question in response.context_data['questions']:
            self.assertTrue(question in questions)


class UserAddQuestionViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(username='testuser1', password='12345')
        test_user1.save()

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('question:add_question'))
        self.assertRedirects(resp, '/users/login/?next=/add-question/')

    def test_logged_in_uses_correct_template(self):
        self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse('question:add_question'))
        self.assertEqual(str(resp.context['user']), 'testuser1')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'questionnaire/add_question.html')


class AjaxViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(username='testuser1', password='12345')
        test_user1.save()
        test_user2 = User.objects.create_user(username='testuser2', password='12345')
        test_user2.save()

        title = "css scale doesn't affect margin"
        text_question = "I have a div that contains several other divs and elements."
        slug = slugify(title)
        test_question = Question.objects.create(id=11, title=title, text_question=text_question, user=test_user1, slug=slug)
        test_question.tags.add('css', 'scale')
        Answer.objects.create(question=test_question, user=test_user2, text_answer='css, scale')

    def test_select_current_answer(self):
        self.client.login(username='testuser1', password='12345')
        self.client.get('/ajax/correct-answer/',
                        {'answer_id': '1', 'correct': 'true'},
                        HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        answer = Answer.objects.get(id=1)
        self.assertTrue(answer.is_correct)

    def test_question_like_unlike_user(self):
        question = Question.objects.get(id=11)
        self.client.login(username='testuser2', password='12345')
        self.client.post('/ajax/like/',
                         {'model_name': 'question', 'id': question.id, 'action': 'like'},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        user = User.objects.get(username='testuser2')
        self.assertTrue(user in question.users_like.all())
        self.client.post('/ajax/like/',
                         {'model_name': 'question', 'id': question.id, 'action': 'unlike'},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertTrue(user not in question.users_like.all())

    def test_answer_like_unlike_user(self):
        answer = Answer.objects.get(id=1)
        self.client.login(username='testuser2', password='12345')
        self.client.post('/ajax/like/',
                         {'model_name': 'answer', 'id': answer.id, 'action': 'like'},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        user = User.objects.get(username='testuser2')
        self.assertTrue(user in answer.users_like.all())

        self.client.post('/ajax/like/',
                         {'model_name': 'answer', 'id': answer.id, 'action': 'unlike'},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertTrue(user not in answer.users_like.all())
