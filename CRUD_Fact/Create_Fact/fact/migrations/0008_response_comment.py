# Generated by Django 5.1 on 2024-11-11 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fact', '0007_fact_deadline'),
    ]

    operations = [
        migrations.AddField(
            model_name='response',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
    ]