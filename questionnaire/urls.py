from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views import QuestionList, TagList, UserList, QuestionListByTag, QuestionDetail, current_answer,CommentAddAnswer,\
    CommentAddQuestion, AddQuestionView, user_like
from .api_views import QuestionViewSet, AnswerViewSet, TagViewSet, CommentViewSet, ProfileViewSet, UserViewSet


router = DefaultRouter()
router.register(r'question', QuestionViewSet)
router.register(r'answer', AnswerViewSet)
router.register(r'tag', TagViewSet)
router.register(r'comment', CommentViewSet)
router.register(r'profile', ProfileViewSet)
router.register(r'user', UserViewSet)

urlpatterns = [
    url(r'^$', QuestionList.as_view(), name="home_page"),
    url(r'^tags/$', TagList.as_view(), name="tags"),
    url(r'^tag/(?P<tag_slug>[-\w]+)/$', QuestionListByTag.as_view(), name="tag_detail"),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', QuestionDetail.as_view(), name='question_detail'),
    url(r'^users/$', UserList.as_view(), name="users"),

    url(r'^add-question/$', AddQuestionView.as_view(), name="add_question"),

    url(r'^add-comment-answer/(?P<id>\d+)/$', CommentAddAnswer.as_view(), name="comment-add-answer"),
    url(r'^add-comment-question/(?P<id>\d+)/$', CommentAddQuestion.as_view(), name="comment-add-question"),

    url(r'^ajax/correct-answer/$', current_answer, name='correct_answer'),
    url(r'^ajax/like/$', user_like, name='user_like'),
    # url(r'^ajax/user/$', suggest_users, name='find_user'),
    url(r'api/', include(router.urls)),
]
