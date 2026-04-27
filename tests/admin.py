from django.contrib import admin
from .models import Test, Question, TestResult

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 5

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('title', 'test_type', 'created_at')
    inlines = [QuestionInline]

@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'score', 'completed_at')
    list_filter = ('test', 'completed_at')
