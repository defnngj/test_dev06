from django.contrib import admin

# Register your models here.
# django 自带一个 admin 后台
from .models import Question, Choice


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'pub_date']
    search_fields = ['question_text']  # 搜索栏


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['choice_text', 'votes', "question"]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
