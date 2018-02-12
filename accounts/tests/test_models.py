from django.contrib.auth.models import User
from django.test import TestCase
from accounts.models import Profile
from questionnaire.models import Question


class ProfileModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='testuser3', password='123123')
        question_1 = Question.objects.create(title='q-1', text_question='q-text-1', user=user)
        question_1.tags.add('django', 'python', 'django-models')
        question_2 = Question.objects.create(title='q-2', text_question='q-text-2', user=user)
        question_2.tags.add('django', 'python')
        question_3 = Question.objects.create(title='q-3', text_question='q-text-3', user=user)
        question_3.tags.add('django')

    def test_object_name(self):
        user = User.objects.get(username='testuser3')
        profile = Profile.objects.get(user=user)
        expected_object_name = profile.user.username
        self.assertEquals(expected_object_name, str(profile))

    def test_get_absolute_url(self):
        user = User.objects.get(username='testuser3')
        profile = Profile.objects.get(user=user)
        profile_url = '/users/profile/%s' % (profile.id)
        self.assertEquals(profile.get_absolute_url(), profile_url)

    def test_best_tag_user(self):
        user = User.objects.get(username='testuser3')
        profile = Profile.objects.get(user=user)
        profile_best_tags = profile.get_best_tags()
        self.assertEqual('django', profile_best_tags[0].name)
        self.assertEqual('python', profile_best_tags[1].name)
        self.assertEqual('django-models', profile_best_tags[2].name)
