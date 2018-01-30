from django.forms import ModelForm
from questionnaire.models import Answer, Comment, Question


class AnswerForm(ModelForm):

    class Meta:
        model = Answer
        fields = ('text_answer', )


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ('comment', )


class AddQuestion(ModelForm):

    class Meta:
        model = Question
        fields = ('title', 'text_question', 'tags', )
