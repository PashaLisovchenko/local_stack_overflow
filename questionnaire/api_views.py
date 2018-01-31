from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet
from taggit.models import Tag
from accounts.models import Profile
from .models import Question, Answer, Comment
from .serializer import QuestionSerializer, AnswerSerializer, TagSerializer, CommentSerializer, ProfileSerializer,\
    UserSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class QuestionViewSet(ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()


class AnswerViewSet(ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()


class TagViewSet(ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class CommentViewSet(ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()


class ProfileViewSet(ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()


class UserViewSet(ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = UserSerializer
    queryset = User.objects.all()
