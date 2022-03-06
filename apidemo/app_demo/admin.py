from django.contrib import admin
from app_demo.models import Task


# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'is_completed', 'owner']


admin.site.register(Task, TaskAdmin)
