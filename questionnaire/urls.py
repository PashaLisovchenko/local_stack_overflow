from django.conf.urls import url
from .views import QuestionList

urlpatterns = [
    url(r'^$', QuestionList.as_view(), name="home_page"),
]
