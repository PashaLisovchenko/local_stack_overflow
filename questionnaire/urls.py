from django.conf.urls import url
from .views import QuestionList, TagList, UserList, QuestionListByTag

urlpatterns = [
    url(r'^$', QuestionList.as_view(), name="home_page"),
    url(r'^tags/$', TagList.as_view(), name="tags"),
    url(r'^tag/(?P<tag_slug>[-\w]+)/$', QuestionListByTag.as_view(), name="tag_detail"),
    url(r'^users/$', UserList.as_view(), name="users"),
]
