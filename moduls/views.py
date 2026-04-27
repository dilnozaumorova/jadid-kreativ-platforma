from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import (
    Lecture, PracticalTask, NormativeDocument, Resource, 
    LectureQuestion, LectureTestResult, TaskSubmission,
    PracticeTopic, PracticeQuestion, PracticeSubmission,
    TablePractice, TableColumn, TableRow, TableSubmission, TableCellAnswer,
    Seminar, SeminarQuestion, SeminarTable, SeminarColumn, SeminarRow, SeminarTableSubmission, SeminarTableCellAnswer, SeminarSubmission,
    CreativeTask, CreativeTaskSubmission
)
from .forms import LectureTestForm, TaskSubmissionForm, PracticeSubmissionForm
from tests.models import TestResult

@user_passes_test(lambda u: u.is_staff)
def statistics(request):
    lecture_results = LectureTestResult.objects.select_related('user', 'lecture').order_by('-completed_at')
    task_submissions = TaskSubmission.objects.select_related('user', 'task').order_by('-submitted_at')
    seminar_submissions = SeminarSubmission.objects.select_related('user', 'question').order_by('-submitted_at')
    seminar_table_submissions = SeminarTableSubmission.objects.select_related('user', 'table').order_by('-submitted_at')
    creative_submissions = CreativeTaskSubmission.objects.select_related('user', 'task').order_by('-submitted_at')
    practice_submissions = PracticeSubmission.objects.select_related('user', 'question').order_by('-submitted_at')
    table_submissions = TableSubmission.objects.select_related('user', 'table').order_by('-submitted_at')
    general_test_results = TestResult.objects.select_related('user', 'test').order_by('-completed_at')
    
    return render(request, 'moduls/statistics.html', {
        'lecture_results': lecture_results,
        'task_submissions': task_submissions,
        'seminar_submissions': seminar_submissions,
        'seminar_table_submissions': seminar_table_submissions,
        'creative_submissions': creative_submissions,
        'practice_submissions': practice_submissions,
        'table_submissions': table_submissions,
        'general_test_results': general_test_results,
    })

@login_required
def my_statistics(request):
    lecture_results = LectureTestResult.objects.filter(user=request.user).select_related('lecture').order_by('-completed_at')
    task_submissions = TaskSubmission.objects.filter(user=request.user).select_related('task').order_by('-submitted_at')
    seminar_submissions = SeminarSubmission.objects.filter(user=request.user).select_related('question').order_by('-submitted_at')
    seminar_table_submissions = SeminarTableSubmission.objects.filter(user=request.user).select_related('table').order_by('-submitted_at')
    creative_submissions = CreativeTaskSubmission.objects.filter(user=request.user).select_related('task').order_by('-submitted_at')
    practice_submissions = PracticeSubmission.objects.filter(user=request.user).select_related('question').order_by('-submitted_at')
    table_submissions = TableSubmission.objects.filter(user=request.user).select_related('table').order_by('-submitted_at')
    general_test_results = TestResult.objects.filter(user=request.user).select_related('test').order_by('-completed_at')
    
    return render(request, 'moduls/my_statistics.html', {
        'lecture_results': lecture_results,
        'task_submissions': task_submissions,
        'seminar_submissions': seminar_submissions,
        'seminar_table_submissions': seminar_table_submissions,
        'creative_submissions': creative_submissions,
        'practice_submissions': practice_submissions,
        'table_submissions': table_submissions,
        'general_test_results': general_test_results,
    })

@login_required
def seminar_list(request):
    seminars = Seminar.objects.all().order_by('created_at')
    
    return render(request, 'moduls/seminar_list.html', {
        'seminars': seminars,
    })

@login_required
def seminar_detail(request, pk):
    seminar = get_object_or_404(Seminar, pk=pk)
    questions = seminar.questions.all()
    tables = seminar.tables.all()
    
    user_question_submissions = []
    user_table_submissions = []
    
    if request.user.is_authenticated:
        user_question_submissions = SeminarSubmission.objects.filter(user=request.user).values_list('question_id', flat=True)
        user_table_submissions = SeminarTableSubmission.objects.filter(user=request.user).values_list('table_id', flat=True)
    
    return render(request, 'moduls/seminar_detail.html', {
        'seminar': seminar,
        'questions': questions,
        'tables': tables,
        'user_question_submissions': user_question_submissions,
        'user_table_submissions': user_table_submissions
    })

@login_required
def seminar_question_detail(request, pk):
    question = get_object_or_404(SeminarQuestion, pk=pk)
    user_submission = SeminarSubmission.objects.filter(user=request.user, question=question).order_by('-submitted_at').first()
    
    if request.method == 'POST':
        text_ans = request.POST.get('text_answer')
        image_ans = request.FILES.get('image_answer')
        SeminarSubmission.objects.create(
            question=question,
            user=request.user,
            text_answer=text_ans,
            image_answer=image_ans
        )
        if question.seminar:
            return redirect('moduls:seminar_detail', pk=question.seminar.id)
        return redirect('moduls:seminar_list')
    
    return render(request, 'moduls/seminar_question_detail.html', {
        'question': question,
        'user_submission': user_submission
    })

@login_required
def seminar_table_detail(request, pk):
    table_obj = get_object_or_404(SeminarTable, pk=pk)
    columns = table_obj.columns.all()
    rows = table_obj.rows.all()
    user_submission = SeminarTableSubmission.objects.filter(user=request.user, table=table_obj).order_by('-submitted_at').first()
    
    if request.method == 'POST':
        submission = SeminarTableSubmission.objects.create(table=table_obj, user=request.user)
        for row in rows:
            for col in columns:
                answer_text = request.POST.get(f'cell_{row.id}_{col.id}', '')
                SeminarTableCellAnswer.objects.create(
                    submission=submission,
                    row=row,
                    column=col,
                    answer=answer_text
                )
        if table_obj.seminar:
            return redirect('moduls:seminar_detail', pk=table_obj.seminar.id)
        return redirect('moduls:seminar_list')
    
    table_data = []
    for row in rows:
        row_data = {'name': row.name, 'cells': []}
        for col in columns:
            answer = ""
            if user_submission:
                ans_obj = user_submission.answers.filter(row=row, column=col).first()
                if ans_obj:
                    answer = ans_obj.answer
            row_data['cells'].append({
                'col_id': col.id,
                'row_id': row.id,
                'answer': answer
            })
        table_data.append(row_data)

    return render(request, 'moduls/seminar_table_detail.html', {
        'table_obj': table_obj,
        'columns': columns,
        'table_data': table_data,
        'user_submission': user_submission,
    })


@login_required
def table_practice_detail(request, pk):
    table_obj = get_object_or_404(TablePractice, pk=pk)
    columns = table_obj.columns.all()
    rows = table_obj.rows.all()
    user_submission = TableSubmission.objects.filter(user=request.user, table=table_obj).order_by('-submitted_at').first()
    
    if request.method == 'POST':
        submission = TableSubmission.objects.create(table=table_obj, user=request.user)
        for row in rows:
            for col in columns:
                answer_text = request.POST.get(f'cell_{row.id}_{col.id}', '')
                TableCellAnswer.objects.create(
                    submission=submission,
                    row=row,
                    column=col,
                    answer=answer_text
                )
        if table_obj.practice:
            return redirect('moduls:practice_detail', pk=table_obj.practice.id)
        return redirect('moduls:practice_list')
    
    # Prepare data for template
    table_data = []
    for row in rows:
        row_data = {'name': row.name, 'cells': []}
        for col in columns:
            answer = ""
            if user_submission:
                ans_obj = user_submission.answers.filter(row=row, column=col).first()
                if ans_obj:
                    answer = ans_obj.answer
            row_data['cells'].append({
                'col_id': col.id,
                'row_id': row.id,
                'answer': answer
            })
        table_data.append(row_data)

    return render(request, 'moduls/table_practice_detail.html', {
        'table_obj': table_obj,
        'columns': columns,
        'table_data': table_data,
        'user_submission': user_submission,
    })

@login_required
def practice_list(request):
    topics = PracticeTopic.objects.all().order_by('created_at')
    
    return render(request, 'moduls/practice_list.html', {
        'topics': topics,
    })

@login_required
def practice_detail(request, pk):
    topic = get_object_or_404(PracticeTopic, pk=pk)
    questions = topic.questions.all()
    tables = topic.tables.all()
    
    user_question_submissions = []
    user_table_submissions = []
    
    if request.user.is_authenticated:
        user_question_submissions = PracticeSubmission.objects.filter(user=request.user).values_list('question_id', flat=True)
        user_table_submissions = TableSubmission.objects.filter(user=request.user).values_list('table_id', flat=True)
    
    return render(request, 'moduls/practice_detail.html', {
        'topic': topic,
        'questions': questions,
        'tables': tables,
        'user_question_submissions': user_question_submissions,
        'user_table_submissions': user_table_submissions
    })

@login_required
def practice_question_detail(request, pk):
    question = get_object_or_404(PracticeQuestion, pk=pk)
    user_submission = PracticeSubmission.objects.filter(user=request.user, question=question).first()
    
    if request.method == 'POST':
        form = PracticeSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.question = question
            submission.user = request.user
            
            # Handle table answer
            if question.question_type == 'table':
                table_data = {}
                for key, value in request.POST.items():
                    if key.startswith('cell_'):
                        table_data[key] = value
                submission.table_answer = table_data
                
            submission.save()
            if question.practice:
                return redirect('moduls:practice_detail', pk=question.practice.id)
            return redirect('moduls:practice_list')
    else:
        form = PracticeSubmissionForm()
    
    return render(request, 'moduls/practice_question_detail.html', {
        'question': question,
        'form': form,
        'user_submission': user_submission
    })

@login_required
def submit_task(request, task_id):
    task = get_object_or_404(PracticalTask, id=task_id)
    if request.method == 'POST':
        form = TaskSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.task = task
            submission.user = request.user
            submission.save()
            return redirect('moduls:task_list')
    else:
        form = TaskSubmissionForm()
    
    return render(request, 'moduls/submit_task.html', {'task': task, 'form': form})

@login_required
def lecture_list(request):
    lectures = list(Lecture.objects.all().order_by('created_at'))
    unlocked_lectures = []
    
    # Logic: 1st lecture is always unlocked. 
    # Next is unlocked if previous is passed with >= 70% in ANY attempt
    for i, lecture in enumerate(lectures):
        if i == 0:
            unlocked_lectures.append(lecture.id)
        else:
            prev_lecture = lectures[i-1]
            if not prev_lecture.questions.exists():
                unlocked_lectures.append(lecture.id)
                continue
                
            # Check if user has ANY result for previous lecture with >= 70%
            results = LectureTestResult.objects.filter(user=request.user, lecture=prev_lecture)
            passed = False
            for res in results:
                if (res.score / res.total_questions) * 100 >= 70:
                    passed = True
                    break
            
            if passed:
                unlocked_lectures.append(lecture.id)
            else:
                break 
                
    return render(request, 'moduls/lecture_list.html', {
        'lectures': lectures,
        'unlocked_lectures': unlocked_lectures
    })

@login_required
def lecture_detail(request, pk):
    lecture = get_object_or_404(Lecture, pk=pk)
    lectures = list(Lecture.objects.all().order_by('created_at'))
    
    # Check if unlocked
    is_unlocked = False
    for i, lec in enumerate(lectures):
        if lec.id == lecture.id:
            if i == 0:
                is_unlocked = True
            else:
                prev_lec = lectures[i-1]
                if not prev_lec.questions.exists():
                    is_unlocked = True
                else:
                    # Any attempt >= 70%?
                    results = LectureTestResult.objects.filter(user=request.user, lecture=prev_lec)
                    for res in results:
                        if (res.score / res.total_questions) * 100 >= 70:
                            is_unlocked = True
                            break
            break
            
    if not is_unlocked:
        return render(request, 'moduls/lecture_locked.html', {'lecture': lecture})

    questions = lecture.questions.all()
    user_result = LectureTestResult.objects.filter(user=request.user, lecture=lecture).order_by('-completed_at').first()
    attempt_count = LectureTestResult.objects.filter(user=request.user, lecture=lecture).count()
    
    # Show form if retake requested OR if no result yet
    show_form = (request.GET.get('retake') == '1') or (not user_result)
    
    form = None
    if show_form and questions.exists():
        form = LectureTestForm(questions=questions)

    percentage = 0
    is_passed = False
    if user_result:
        percentage = (user_result.score / user_result.total_questions) * 100
        is_passed = (percentage >= 70)

    return render(request, 'moduls/lecture_detail.html', {
        'lecture': lecture,
        'questions': questions,
        'form': form,
        'user_result': user_result,
        'percentage': percentage,
        'is_passed': is_passed,
        'show_form': show_form,
        'attempt_count': attempt_count
    })

@login_required
def retake_lecture_test(request, lecture_id):
    lecture = get_object_or_404(Lecture, id=lecture_id)
    # Don't delete! History is important. Just redirect to show the form again.
    # We need to modify lecture_detail to show the form even if user_result exists IF coming from retake or if we want to allow multiple.
    return redirect('moduls:lecture_detail', pk=lecture.id)

@login_required
def submit_lecture_test(request, lecture_id):
    lecture = get_object_or_404(Lecture, id=lecture_id)
    questions = lecture.questions.all()
    
    if request.method == 'POST':
        form = LectureTestForm(request.POST, questions=questions)
        if form.is_valid():
            score = 0
            for question in questions:
                user_answer = form.cleaned_data.get(f'question_{question.id}')
                if user_answer == question.correct_option:
                    score += 1
            
            # Save result
            LectureTestResult.objects.create(
                user=request.user,
                lecture=lecture,
                score=score,
                total_questions=questions.count()
            )
            return redirect('moduls:lecture_detail', pk=lecture.id)
    
    return redirect('moduls:lecture_detail', pk=lecture.id)

@login_required
def task_list(request):
    tasks = PracticalTask.objects.all()
    user_submissions = []
    if request.user.is_authenticated:
        user_submissions = TaskSubmission.objects.filter(user=request.user).values_list('task_id', flat=True)
    
    return render(request, 'moduls/task_list.html', {
        'tasks': tasks,
        'user_submissions': user_submissions
    })

@login_required
def normative_documents_list(request):
    documents = NormativeDocument.objects.all()
    return render(request, 'moduls/normative_documents_list.html', {'documents': documents})

@login_required
def resource_list(request):
    resources = Resource.objects.all()
    return render(request, 'moduls/resource_list.html', {'resources': resources})

@login_required
def creative_tasks(request):
    tasks = CreativeTask.objects.all()
    user_submissions = []
    if request.user.is_authenticated:
        user_submissions = CreativeTaskSubmission.objects.filter(user=request.user).values_list('task_id', flat=True)
    
    return render(request, 'moduls/creative_tasks.html', {
        'tasks': tasks,
        'user_submissions': user_submissions
    })

@login_required
def creative_task_detail(request, pk):
    task = get_object_or_404(CreativeTask, pk=pk)
    user_submission = CreativeTaskSubmission.objects.filter(user=request.user, task=task).order_by('-submitted_at').first()
    
    if request.method == 'POST':
        if task.task_type == 'test':
            selected = request.POST.get('option')
            is_correct = (selected == task.correct_option)
            CreativeTaskSubmission.objects.create(
                task=task,
                user=request.user,
                selected_option=selected,
                is_correct=is_correct,
                is_checked=True,
                score=100 if is_correct else 0
            )
        else:
            text_ans = request.POST.get('text_answer', '')
            file_ans = request.FILES.get('file_answer')
            CreativeTaskSubmission.objects.create(
                task=task,
                user=request.user,
                text_answer=text_ans,
                file_answer=file_ans
            )
        return redirect('moduls:creative_tasks')
        
    return render(request, 'moduls/creative_task_detail.html', {
        'task': task,
        'user_submission': user_submission
    })
