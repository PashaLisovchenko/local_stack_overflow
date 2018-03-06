from django.contrib.auth.models import User
from django.test import TestCase
from django.utils.text import slugify
from taggit.models import Tag
from questionnaire.models import Question, DescriptionTag


class QuestionModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        title = "css scale doesn't affect margin"
        text_question = "I have a div that contains several other divs and elements."
        user = User.objects.create(username='pasha', password='12345')
        slug = slugify(title)
        q = Question.objects.create(id=1, title=title, text_question=text_question, user=user, slug=slug)
        q.tags.add('css', 'scale')

    def test_object_slug_name(self):
        q = Question.objects.get(id=1)
        expected_object_name = '%s' % (q.slug)
        self.assertEquals(expected_object_name, str(q))

    def test_get_absolute_url(self):
        q = Question.objects.get(id=1)
        question_url = '/%s/%s/' % (q.id, q.slug)
        self.assertEquals(q.get_absolute_url(), question_url)


class TagModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Tag.objects.create(name='html')

    def test_post_save_create_description_object(self):
        tag = Tag.objects.get(name='html')
        description_object = DescriptionTag.objects.filter(tag=tag).exists()
        self.assertTrue(description_object)

