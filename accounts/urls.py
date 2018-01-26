from django.conf.urls import url
from .views import LoginView, LogoutView, CreateUser, ProfileView, UpdateProfile

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^signup/$', CreateUser.as_view(), name="signup"),
    url(r'^logout/$', LogoutView.as_view(), name="logout"),
    url(r'^profile/(?P<id>\d+)$', ProfileView.as_view(), name="profile"),
    url(r'^(?P<id>\d+)/update_profile$', UpdateProfile.as_view(), name="update_profile"),
]
