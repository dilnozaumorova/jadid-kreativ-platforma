from django.contrib import admin
from .models import (
    Lecture, PracticalTask, NormativeDocument, Resource, 
    LectureQuestion, LectureTestResult, PracticeTopic, PracticeQuestion, PracticeSubmission,
    TablePractice, TableColumn, TableRow, TableSubmission, TableCellAnswer,
    Seminar, SeminarQuestion, SeminarTable, SeminarColumn, SeminarRow, SeminarTableSubmission, SeminarTableCellAnswer, SeminarSubmission,
    CreativeTask, CreativeTaskSubmission, TaskSubmission
)
from django import forms

@admin.register(PracticeTopic)
class PracticeTopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')

@admin.register(Seminar)
class SeminarAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')

class SeminarColumnInline(admin.TabularInline):
    model = SeminarColumn
    extra = 3

class SeminarRowInline(admin.TabularInline):
    model = SeminarRow
    extra = 3

@admin.register(SeminarTable)
class SeminarTableAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    inlines = [SeminarColumnInline, SeminarRowInline]

@admin.register(SeminarQuestion)
class SeminarQuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'question_type', 'created_at')

@admin.register(SeminarSubmission)
class SeminarSubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'score', 'is_checked', 'submitted_at')
    list_editable = ('score', 'is_checked')

@admin.register(SeminarTableSubmission)
class SeminarTableSubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'table', 'score', 'is_checked', 'submitted_at')
    list_editable = ('score', 'is_checked')

class TableColumnInline(admin.TabularInline):
    model = TableColumn
    extra = 3

class TableRowInline(admin.TabularInline):
    model = TableRow
    extra = 3

@admin.register(TablePractice)
class TablePracticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    inlines = [TableColumnInline, TableRowInline]

@admin.register(PracticeQuestion)
class PracticeQuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'question_type', 'created_at')

@admin.register(PracticeSubmission)
class PracticeSubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'score', 'is_checked', 'submitted_at')
    list_editable = ('score', 'is_checked')

@admin.register(TableSubmission)
class TableSubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'table', 'score', 'is_checked', 'submitted_at')
    list_editable = ('score', 'is_checked')

@admin.register(CreativeTask)
class CreativeTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task_type', 'created_at')

@admin.register(CreativeTaskSubmission)
class CreativeTaskSubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'task', 'score', 'is_checked', 'submitted_at')
    list_editable = ('score', 'is_checked')

@admin.register(LectureTestResult)
class LectureTestResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'lecture', 'score', 'total_questions', 'completed_at')

class QuestionInline(admin.TabularInline):
    model = LectureQuestion
    extra = 4

@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    inlines = [QuestionInline]
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'content':  # field nomi
            kwargs['widget'] = forms.Textarea(attrs={
                'rows': 20,
                'cols': 120,
            })
        return super().formfield_for_dbfield(db_field, **kwargs)

@admin.register(PracticalTask)
class PracticalTaskAdmin(admin.ModelAdmin):
    list_display = ('task_name', 'deadline', 'created_at')

@admin.register(NormativeDocument)
class NormativeDocumentAdmin(admin.ModelAdmin):
    list_display = ('document_name', 'created_at')

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('resource_name', 'created_at')

@admin.register(TaskSubmission)
class TaskSubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'task', 'score', 'is_checked', 'submitted_at')
    list_editable = ('score', 'is_checked')
