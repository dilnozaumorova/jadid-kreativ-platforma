from django.db import models
from django.conf import settings

class Test(models.Model):
    TYPE_CHOICES = [
        ('entry', 'Kirish testi'),
        ('exit', 'Chiqish testi'),
    ]
    title = models.CharField(max_length=255)
    test_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.get_test_type_display()})"

class Question(models.Model):
    TYPE_CHOICES = [
        ('gap_fill', 'Bo\'sh joyni to\'ldirish'),
        ('mcq', 'Ko\'p variantli (A, B, C, D)'),
    ]
    test = models.ForeignKey(Test, related_name='questions', on_delete=models.CASCADE)
    question_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='gap_fill')
    text = models.TextField(help_text="Savol matni. MCQ uchun variantlarni quyida to'ldiring.")
    
    # Gap Fill correct answer or MCQ correct option (A, B, C, D)
    correct_answer = models.CharField(
        max_length=255, 
        help_text="Gap Fill bo'lsa: to'g'ri so'zni yozing. MCQ bo'lsa: to'g'ri variant harfini yozing (A, B, C yoki D)."
    )
    
    # MCQ options
    option_a = models.CharField(max_length=255, blank=True, null=True)
    option_b = models.CharField(max_length=255, blank=True, null=True)
    option_c = models.CharField(max_length=255, blank=True, null=True)
    option_d = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"[{self.get_question_type_display()}] {self.text[:50]}"

class TestResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.IntegerField()
    total_questions = models.IntegerField(default=5)
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.test.title} - {self.score}/{self.total_questions}"

