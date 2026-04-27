from django.db import models
from tests.models import Test

class Lecture(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='lectures/images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class LectureQuestion(models.Model):
    lecture = models.ForeignKey(Lecture, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])

    def __str__(self):
        return f"Question for {self.lecture.title}"

class LectureTestResult(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.lecture.title} - {self.score}"

class PracticalTask(models.Model):
    task_name = models.CharField(max_length=255)
    task_description = models.TextField()
    deadline = models.DateTimeField()
    file_upload = models.FileField(upload_to='tasks/submissions/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.task_name

class NormativeDocument(models.Model):
    document_name = models.CharField(max_length=255)
    file_upload = models.FileField(upload_to='normative_docs/', help_text="PDF/DOC file")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.document_name

class Resource(models.Model):
    resource_name = models.CharField(max_length=255)
    resource_link = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.resource_name

class TaskSubmission(models.Model):
    task = models.ForeignKey(PracticalTask, related_name='submissions', on_delete=models.CASCADE)
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    file = models.FileField(upload_to='student_submissions/')
    comment = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0, verbose_name="Baholash (Ball)")
    is_checked = models.BooleanField(default=False, verbose_name="Tekshirildi")

    def __str__(self):
        return f"{self.user.username} - {self.task.task_name}"

class PracticeTopic(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class PracticeQuestion(models.Model):
    QUESTION_TYPES = (
        ('image', 'Image Submission'),
        ('text', 'Text Submission'),
    )
    practice = models.ForeignKey(PracticeTopic, related_name='questions', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class TablePractice(models.Model):
    practice = models.ForeignKey(PracticeTopic, related_name='tables', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class TableColumn(models.Model):
    table = models.ForeignKey(TablePractice, related_name='columns', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class TableRow(models.Model):
    table = models.ForeignKey(TablePractice, related_name='rows', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class TableSubmission(models.Model):
    table = models.ForeignKey(TablePractice, related_name='submissions', on_delete=models.CASCADE)
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0, verbose_name="Baholash (Ball)")
    is_checked = models.BooleanField(default=False, verbose_name="Tekshirildi")

    def __str__(self):
        return f"{self.user.username} - {self.table.title}"

class TableCellAnswer(models.Model):
    submission = models.ForeignKey(TableSubmission, related_name='answers', on_delete=models.CASCADE)
    column = models.ForeignKey(TableColumn, on_delete=models.CASCADE)
    row = models.ForeignKey(TableRow, on_delete=models.CASCADE)
    answer = models.TextField()

class PracticeSubmission(models.Model):
    question = models.ForeignKey(PracticeQuestion, related_name='submissions', on_delete=models.CASCADE)
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    text_answer = models.TextField(blank=True, null=True)
    image_answer = models.ImageField(upload_to='practice_submissions/', blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0, verbose_name="Baholash (Ball)")
    is_checked = models.BooleanField(default=False, verbose_name="Tekshirildi")

    def __str__(self):
        return f"{self.user.username} - {self.question.title}"

class Seminar(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class SeminarQuestion(models.Model):
    QUESTION_TYPES = (
        ('image', 'Image Submission'),
        ('text', 'Text Submission'),
    )
    seminar = models.ForeignKey(Seminar, related_name='questions', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class SeminarTable(models.Model):
    seminar = models.ForeignKey(Seminar, related_name='tables', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class SeminarColumn(models.Model):
    table = models.ForeignKey(SeminarTable, related_name='columns', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class SeminarRow(models.Model):
    table = models.ForeignKey(SeminarTable, related_name='rows', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class SeminarTableSubmission(models.Model):
    table = models.ForeignKey(SeminarTable, related_name='submissions', on_delete=models.CASCADE)
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0, verbose_name="Baholash (Ball)")
    is_checked = models.BooleanField(default=False, verbose_name="Tekshirildi")

    def __str__(self):
        return f"{self.user.username} - {self.table.title}"

class SeminarTableCellAnswer(models.Model):
    submission = models.ForeignKey(SeminarTableSubmission, related_name='answers', on_delete=models.CASCADE)
    column = models.ForeignKey(SeminarColumn, on_delete=models.CASCADE)
    row = models.ForeignKey(SeminarRow, on_delete=models.CASCADE)
    answer = models.TextField()

class SeminarSubmission(models.Model):
    question = models.ForeignKey(SeminarQuestion, related_name='submissions', on_delete=models.CASCADE)
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    text_answer = models.TextField(blank=True, null=True)
    image_answer = models.ImageField(upload_to='seminar_submissions/', blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0, verbose_name="Baholash (Ball)")
    is_checked = models.BooleanField(default=False, verbose_name="Tekshirildi")

    def __str__(self):
        return f"{self.user.username} - {self.question.title}"

class CreativeTask(models.Model):
    TASK_TYPES = (
        ('test', 'Test (A,B,C,D)'),
        ('submission', 'Javob yuborish (Matn/Fayl)'),
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='creative_tasks/', blank=True, null=True)
    task_type = models.CharField(max_length=20, choices=TASK_TYPES)
    
    option_a = models.CharField(max_length=255, blank=True, null=True)
    option_b = models.CharField(max_length=255, blank=True, null=True)
    option_c = models.CharField(max_length=255, blank=True, null=True)
    option_d = models.CharField(max_length=255, blank=True, null=True)
    correct_option = models.CharField(max_length=1, choices=(('A','A'),('B','B'),('C','C'),('D','D')), blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class CreativeTaskSubmission(models.Model):
    task = models.ForeignKey(CreativeTask, related_name='submissions', on_delete=models.CASCADE)
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    
    selected_option = models.CharField(max_length=1, blank=True, null=True)
    is_correct = models.BooleanField(default=False)
    
    text_answer = models.TextField(blank=True, null=True)
    file_answer = models.FileField(upload_to='creative_submissions/', blank=True, null=True)
    
    submitted_at = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0, verbose_name="Baholash (Ball)")
    is_checked = models.BooleanField(default=False, verbose_name="Tekshirildi")

    def __str__(self):
        return f"{self.user.username} - {self.task.title}"


from django.db.models.signals import post_delete
from django.dispatch import receiver

@receiver(post_delete)
def delete_files_on_instance_delete(sender, instance, **kwargs):
    """Model o'chirilganda unga tegishli faylni Supabase'dan ham o'chirish"""
    for field in instance._meta.fields:
        if isinstance(field, (models.FileField, models.ImageField)):
            file = getattr(instance, field.name)
            if file:
                try:
                    file.delete(save=False)
                except Exception as e:
                    print(f"Faylni o'chirishda xatolik: {e}")

