# Generated by Django 5.1 on 2024-12-04 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('student', 'Student'), ('professor', 'Professor')], max_length=10),
        ),
    ]
