from django import forms
from .models import LectureQuestion, TaskSubmission, PracticeSubmission

class PracticeSubmissionForm(forms.ModelForm):
    class Meta:
        model = PracticeSubmission
        fields = ['text_answer', 'image_answer']
        widgets = {
            'text_answer': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Javobingizni shu yerga yozing...'}),
            'image_answer': forms.FileInput(attrs={'class': 'form-control'}),
        }

class TaskSubmissionForm(forms.ModelForm):
    class Meta:
        model = TaskSubmission
        fields = ['file', 'comment']
        widgets = {
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ixtiyoriy izoh...'}),
        }

class LectureTestForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions', [])
        super().__init__(*args, **kwargs)
        for question in questions:
            choices = [
                ('A', f"A) {question.option_a}"),
                ('B', f"B) {question.option_b}"),
                ('C', f"C) {question.option_c}"),
                ('D', f"D) {question.option_d}"),
            ]
            self.fields[f'question_{question.id}'] = forms.ChoiceField(
                label=question.text,
                choices=choices,
                widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
                required=True
            )
