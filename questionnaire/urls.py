from django.conf.urls import url
from .views import QuestionList, TagList, UserList, QuestionListByTag, QuestionDetail, current_answer,CommentAddAnswer,\
    CommentAddQuestion, AddQuestionView, suggest_users

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
    url(r'^ajax/user/$', suggest_users, name='find_user'),
]
