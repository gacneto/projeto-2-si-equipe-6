from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('professor', 'Professor'),
        ('student', 'Aluno'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

class Course(models.Model):
    name = models.CharField(max_length=100)
    period = models.CharField(max_length=20)
    professors = models.ManyToManyField('User', limit_choices_to={'user_type': 'professor'})

    def __str__(self):
        return f"{self.name} - {self.period}"

class FACT(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    criteria = models.ManyToManyField('Criterion')
    deadline = models.DateTimeField()
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"FACT for {self.course}"

class Criterion(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Evaluation(models.Model):
    fact = models.ForeignKey(FACT, on_delete=models.CASCADE)
    evaluator = models.ForeignKey('User', related_name='evaluator', on_delete=models.CASCADE)
    evaluated = models.ForeignKey('User', related_name='evaluated', on_delete=models.CASCADE)
    criterion = models.ForeignKey(Criterion, on_delete=models.CASCADE)
    score = models.IntegerField()
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Evaluation from {self.evaluator} to {self.evaluated}"

class Enrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey('User', limit_choices_to={'user_type': 'student'}, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student} in {self.course}"
