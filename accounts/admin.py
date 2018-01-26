from django.contrib import admin
from django.utils.html import format_html
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','show_git_url', 'bio', 'birth_date', 'location']

    def show_git_url(self, obj):
        return format_html("<a href='{url}'>{url}</a>", url=obj.link_github)

    show_git_url.short_description = "GitHub URL"


admin.site.register(Profile, ProfileAdmin)

