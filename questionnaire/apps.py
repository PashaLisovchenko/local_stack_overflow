from django.apps import AppConfig


class QuestionnaireConfig(AppConfig):
    name = 'questionnaire'

    def ready(self):
        from actstream import registry
        registry.register(self.get_model('Question'))
        registry.register(self.get_model('Answer'))
        registry.register(self.get_model('Comment'))
        from django.contrib.auth.models import User
        registry.register(User)
