from django.db import models

class Fact(models.Model):
    title = models.CharField(max_length=200)
    deadline = models.DateTimeField()
    is_draft = models.BooleanField(default=True)
    num_groups = models.PositiveIntegerField()
    is_resolved = models.BooleanField(default=False)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Group(models.Model):
    fact = models.ForeignKey(Fact, on_delete=models.CASCADE, related_name="groups")
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.fact.title} - {self.name}"


class Member(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='members')  
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.group.name} - {self.name}"


class Question(models.Model):
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text


class Response(models.Model):
    fact = models.ForeignKey(Fact, on_delete=models.CASCADE, related_name="responses")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, null=True, on_delete=models.CASCADE, related_name='responses')
    score = models.IntegerField(choices=[(i, str(i)) for i in range(0, 11)])  # Pontuação de 0 a 10
    comment = models.TextField(blank=True, null=True)  # Novo campo para comentário

    def __str__(self):
        group_name = self.group.name if self.group else "Nenhum grupo"
        question_text = self.question.text if self.question else "Sem pergunta"
        member_name = self.member.name if self.member else "Nenhum membro"
        return f"{group_name} - {question_text}: {self.score} (Membro: {member_name})"
