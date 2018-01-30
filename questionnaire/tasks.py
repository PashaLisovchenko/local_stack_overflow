from celery import shared_task
from .models import Answer
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
