import datetime
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    title = models.CharField(max_length=60)
    slug = models.SlugField(max_length=60, db_index=True)
    text_question = models.TextField(max_length=500)
    tags = TaggableManager()
    users_like = models.ManyToManyField(User, related_name='question_liked', blank=True)
    # dislike
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        index_together = (('id', 'slug'),)
        ordering = ('-created', )

    def __str__(self):
        return self.user.username + ', ' + self.slug

    def get_absolute_url(self):
        return reverse('question:question_detail', args=[self.id, self.slug])


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answer') # неуверен что нужен on_delete
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text_answer = models.TextField(max_length=500)
    is_correct = models.BooleanField(default=False)
    users_like = models.ManyToManyField(User, related_name='answer_liked', blank=True)
    # dislike
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username + ', ' + self.text_answer

    # def get_absolute_url(self):
    #     return reverse('question:detail_question', args=[self.id, self.slug])


class Comment(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    user = models.ForeignKey(User, related_name='comments')
    comment = models.CharField(max_length=300)
    added_at = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        ordering = ('added_at',)
