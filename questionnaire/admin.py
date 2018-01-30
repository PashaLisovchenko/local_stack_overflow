from django.contrib import admin
from .models import Question, Answer, Comment


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['user','slug', 'text_question', 'created', 'updated']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Question, QuestionAdmin)


class AnswerAdmin(admin.ModelAdmin):
    list_display = ['user', 'question', 'text_answer', 'is_correct', ]


admin.site.register(Answer, AnswerAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'comment', 'content_type', 'object_id', 'content_object', ]


admin.site.register(Comment, CommentAdmin)