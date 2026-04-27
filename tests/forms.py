from django import forms

class GapFillTestForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions', [])
        super().__init__(*args, **kwargs)
        for i, question in enumerate(questions):
            field_name = f'question_{question.id}'
            if question.question_type == 'mcq':
                choices = [
                    ('A', f"A) {question.option_a}"),
                    ('B', f"B) {question.option_b}"),
                    ('C', f"C) {question.option_c}"),
                    ('D', f"D) {question.option_d}"),
                ]
                field = forms.ChoiceField(
                    label=question.text,
                    choices=choices,
                    widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
                    required=True
                )
                field.is_mcq = True
                self.fields[field_name] = field
            else: # gap_fill
                self.fields[field_name] = forms.CharField(
                    label=question.text,
                    widget=forms.TextInput(attrs={'placeholder': '______', 'class': 'form-control'}),
                    required=True
                )
