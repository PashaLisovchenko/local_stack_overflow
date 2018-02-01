from taggit.models import Tag
import urllib.request
from lxml.html import fromstring
from .models import Answer, DescriptionTag
from django.core.mail import send_mail
from local_stack_overflow.celery import app


@app.task
def send_message(answer_id):
    answer = Answer.objects.get(pk=answer_id)
    subject = '({}) answer you question.'.format(answer.user.username)
    email_from = answer.user.email
    email_to = answer.question.user.email
    question_url = "http://127.0.0.1:8000" + answer.question.get_absolute_url()
    message = 'On your question "{}" user "{}" replied "{}" look more {}.'.format(answer.question.title,
                                                                                  answer.user.username,
                                                                                  answer.text_answer,
                                                                                  question_url)

    send_mail(subject, message, email_from, [email_to])
    print('send email')


@app.task
def parse_stack(tag_id):
    tag = Tag.objects.get(id=tag_id)
    page_url = 'https://stackoverflow.com/tags/' + tag.slug + '/info'
    response = urllib.request.urlopen(page_url).read()
    page = fromstring(response)
    description_tag = page.xpath('//div[@class="post-text"]/div[@class="welovestackoverflow"]/p')
    description_tag = description_tag[0].text.strip()
    descr_tag = DescriptionTag.objects.get(tag=tag)
    descr_tag.description = description_tag
    descr_tag.save()
    print(tag)
    print('description_tag saved')
