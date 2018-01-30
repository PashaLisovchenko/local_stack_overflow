from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.urlresolvers import reverse
from taggit.models import Tag

from questionnaire.models import Question


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    link_github = models.URLField(max_length=100, blank=True)
    image = models.ImageField(blank=True, null=True, upload_to='profile_image/', default='profile_image/default.png')
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=('-created', )

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('accounts:profile', args=[self.user.id])

    def get_best_tags(self):
        questions = Question.objects.filter(user=self.user)
        tags = Tag.objects.filter(question__in=questions)
        best_tags = tags.annotate(same_tags=Count('name')).order_by('-same_tags')[:3]
        return best_tags


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
