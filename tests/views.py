from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Test, Question, TestResult
from .forms import GapFillTestForm

@login_required
def test_list(request):
    tests = Test.objects.all()
    return render(request, 'tests/test_list.html', {'tests': tests})

@login_required
def submit_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    questions = test.questions.all()
    
    if request.method == 'POST':
        form = GapFillTestForm(request.POST, questions=questions)
        if form.is_valid():
            score = 0
            for question in questions:
                user_answer = form.cleaned_data.get(f'question_{question.id}', '').strip().lower()
                correct_answer = question.correct_answer.strip().lower()
                if user_answer == correct_answer:
                    score += 1
            
            # Save result
            result = TestResult.objects.create(
                user=request.user,
                test=test,
                score=score,
                total_questions=len(questions)
            )
            return redirect('tests:test_result', result_id=result.id)
    else:
        form = GapFillTestForm(questions=questions)
    
    return render(request, 'tests/take_test.html', {'test': test, 'form': form})

@login_required
def test_result(request, result_id):
    result = get_object_or_404(TestResult, id=result_id, user=request.user)
    return render(request, 'tests/test_result.html', {'result': result})
