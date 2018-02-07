from datetime import timedelta
from celery.task import periodic_task
from django.template.defaultfilters import lower
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


@periodic_task(run_every=timedelta(seconds=10))
def parse():
    tag_descr = DescriptionTag.objects.filter(description='')
    print('Check needed parse?')
    if tag_descr:
        print('PARSE DESCRIPTION TAG...')
        for descr in tag_descr:
            tag = descr.tag
            page_url = 'https://stackoverflow.com/tags/' + lower(tag.name) + '/info'
            try:
                response = urllib.request.urlopen(page_url).read()
                page = fromstring(response)
                try:
                    description_tag = page.xpath('//div[@class="post-text"]/div[@class="welovestackoverflow"]/p')
                    description_tag = description_tag[0].text.strip()
                except IndexError:
                    description_tag = page.xpath('//div[@class="question"]/div[@class="welovestackoverflow"]/div/p[1]')
                    description_tag = description_tag[0].text.strip()
            except OSError:
                description_tag = 'Unknown tag'
            descr.description = description_tag
            descr.save()
            print(tag)
            print('description_tag saved')