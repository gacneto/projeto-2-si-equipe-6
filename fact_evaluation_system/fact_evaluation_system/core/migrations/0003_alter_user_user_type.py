# Generated by Django 5.1 on 2024-12-04 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_user_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('professor', 'Professor'), ('student', 'Aluno')], max_length=10),
        ),
    ]