import datetime
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.db.models import signals
from django.contrib.auth.models import User
from markdownx.utils import markdownify
from taggit.managers import TaggableManager
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from taggit.models import Tag


class DescriptionTag(models.Model):
    tag = models.OneToOneField(Tag, related_name='description')
    description = models.TextField()


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, db_index=True)
    text_question = models.TextField()
    tags = TaggableManager()
    users_like = models.ManyToManyField(User, related_name='question_liked', blank=True)
    # dislike
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        index_together = (('id', 'slug'),)
        ordering = ('-created', )

    @property
    def formatted_markdown(self):
        return markdownify(self.text_question)

    def __str__(self):
        return self.user.username + ', ' + self.slug

    def get_absolute_url(self):
        return reverse('question:question_detail', args=[self.id, self.slug])

    def get_tags_display(self):
        return self.tags.values_list('name', flat=True)


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answer')  # I'm not sure what need on_delete
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text_answer = models.TextField()
    is_correct = models.BooleanField(default=False)
    users_like = models.ManyToManyField(User, related_name='answer_liked', blank=True)
    # dislike
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        # ordering = ('-is_correct', '-created',)
        ordering = ('-created',)

    def __str__(self):
        return self.user.username + ', ' + self.text_answer

    @property
    def formatted_markdown(self):
        return markdownify(self.text_answer)
    # def get_absolute_url(self):
    #     return reverse('question:detail_question', args=[self.id, self.slug])


def send_email_question_user(sender, instance, signal, *args, **kwargs):
    from .tasks import send_message
    created = kwargs.get('created')
    if created:
        send_message.delay(instance.pk)


signals.post_save.connect(send_email_question_user, sender=Answer)


class Comment(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    user = models.ForeignKey(User, related_name='comments')
    comment = models.TextField(max_length=400)
    added_at = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        ordering = ('added_at',)


def parse_stack_description_tag(sender, instance, signal, *args, **kwargs):
    from .tasks import parse_stack
    DescriptionTag.objects.get_or_create(tag=instance)
    if not instance.description.description:
        parse_stack.delay(instance.pk)


signals.post_save.connect(parse_stack_description_tag, sender=Tag)

