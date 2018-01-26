from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.views.generic import FormView, View, CreateView, DetailView, UpdateView
from questionnaire.models import Question, Answer
from .forms import RegisterForm, UpdateProfileForm
from .models import User, Profile


class LoginView(FormView):
    template_name = 'accounts/base_account.html'
    form_class = AuthenticationForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['section'] = 'Login'
        return context

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
            else:
                return HttpResponse("Inactive user.")
        else:
            return HttpResponseRedirect(settings.LOGIN_URL)


class CreateUser(CreateView):
    model = User
    template_name = 'accounts/base_account.html'
    form_class = RegisterForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(CreateUser, self).get_context_data(**kwargs)
        context['section'] = 'CreateUser'
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            user = self.form_valid(form)
            login(request, user)
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        return user


class LogoutView(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(settings.LOGIN_URL)


class ProfileView(DetailView):
    template_name = 'accounts/profile.html'
    model = User
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        question_list = Question.objects.filter(user=self.object)
        context['user_question_list'] = question_list
        answer_list = Answer.objects.filter(user=self.object)
        context['user_answer_list'] = answer_list
        return context


class UpdateProfile(UpdateView):
    model = User
    fields = ['username', 'email', 'first_name', 'last_name']
    template_name = 'accounts/update_profile_form.html'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super(UpdateProfile, self).get_context_data(**kwargs)
        user = self.object
        form_class = UpdateProfileForm(data=vars(user.profile))
        context['form_profile'] = form_class
        return context

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        user_profile = Profile.objects.get(user=user)
        req_file = request.FILES
        req_post = request.POST
        user_profile.bio = req_post['bio']
        user_profile.birth_date = req_post['birth_date']
        user_profile.link_github = req_post['link_github']
        user_profile.location = req_post['location']
        if not req_file:
            user_profile.save()
        else:
            user_profile.image = req_file['image']
            user_profile.save()
        return super(UpdateProfile, self).post(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        user = self.get_object()
        return reverse_lazy('accounts:profile', kwargs={'id': user.id})
