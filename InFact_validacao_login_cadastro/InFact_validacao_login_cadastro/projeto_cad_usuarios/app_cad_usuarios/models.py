from django.db import models

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nome = models.TextField(max_length=255)
    matricula = models.TextField(max_length=255)
    email = models.TextField(max_length=255, )
    senha = models.TextField(max_length=255)

