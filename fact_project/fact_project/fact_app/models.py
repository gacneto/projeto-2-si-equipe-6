from django.db import models
from django.contrib.auth.models import AbstractUser 
from django.conf import settings 

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('teacher', 'Professor'),
        ('student', 'Aluno'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return self.username

class Course(models.Model):
    name = models.CharField(max_length=100)
    period = models.IntegerField()
    professor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='courses'
    )

    def __str__(self):
        return f"{self.name} ({self.period}º período)"

class Criterion(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Fact(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    criteria = models.ManyToManyField(Criterion, through='FactScore')
    date_submitted = models.DateTimeField(auto_now_add=True)

    def average_score(self):
        scores = self.factscore_set.all()
        if scores:
            return sum(score.value for score in scores) / scores.count()
        return 0

class FactScore(models.Model):
    fact = models.ForeignKey('Fact', on_delete=models.CASCADE)
    criterion = models.ForeignKey(Criterion, on_delete=models.CASCADE)
    value = models.FloatField()

    def __str__(self):
        return f"{self.criterion.name}: {self.value}"