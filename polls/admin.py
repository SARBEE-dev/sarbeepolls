from django.contrib import admin
from .models import Choice, Question

class ChoiceInLine(admin.StackedInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['question_text']}), ('Date information',
                {'fields': ['pub_date'], 'classes':['collapse']}), ]
    inlines = [ChoiceInLine]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)

admin.site.site_header = 'SARBEE Admin'
admin.site.site_title = 'Pollster Admin Area'
admin.site.index_title = 'Welcome to the SARBEE polls admin area'
