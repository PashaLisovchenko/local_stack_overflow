from django.forms import ModelForm, DateField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.extras.widgets import SelectDateWidget
from accounts.models import Profile


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email', )


class UpdateProfileForm(ModelForm):
    # birth_date = DateField(widget=SelectDateWidget, required=False)

    class Meta:
        model = Profile
        # fields = ('link_github', 'image', 'bio', 'location', 'birth_date')
        exclude = ['created', 'user']
