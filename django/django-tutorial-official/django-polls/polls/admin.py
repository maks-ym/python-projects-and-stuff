# Register your models here.
from django.contrib import admin

from .models import Choice, Question


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                  {'fields': ['question_text']}),
        ('Date innformation',   {'fields': ['pub_date']})
    ]
    inlines = [ChoiceInline]
    list_display = ['question_text', 'pub_date', 'was_published_recently']
    sortable_by = ['question_text']
    list_filter = ['pub_date']
    search_fields = ['question_text']
    search_help_text = "Can type several words (blah-blah-blah it is a custom text)"
    date_hierarchy = 'pub_date'
    # view_on_site = True
    # list_per_page = 2


admin.site.register(Question, QuestionAdmin)
