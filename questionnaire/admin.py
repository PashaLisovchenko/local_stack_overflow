from django.contrib import admin
from .models import Question


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['user','slug', 'text_question', 'created', 'updated']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Question, QuestionAdmin)