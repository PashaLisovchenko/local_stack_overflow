from django.contrib.auth.models import User
from taggit.models import Tag
from accounts.models import Profile
from .models import Answer, Question, Comment
from rest_framework import serializers
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('id', 'user')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name')


class AnswerSerializer(serializers.ModelSerializer):
    # question = QuestionSerializer()

    class Meta:
        model = Answer
        fields = ('user', 'question', 'text_answer', 'is_correct', 'users_like', 'created')


class QuestionSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ('user', 'title', 'tags', 'text_question', 'answers', 'users_like', 'created')



class ActivityObjectRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        if isinstance(value, Question):
            return 'Question: ' + value.title
        elif isinstance(value, Answer):
            return 'Answer: ' + value.text_answer
        raise Exception('Unexpected type of tagged object')


class CommentSerializer(serializers.ModelSerializer):
    content_object = ActivityObjectRelatedField(read_only=True)
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = ('user', 'comment', 'added_at', 'content_object')
