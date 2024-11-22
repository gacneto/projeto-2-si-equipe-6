from django.contrib import admin
from .models import Fact, Group, Member, Question, Response

@admin.register(Fact)
class FactAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_draft', 'num_groups', 'created_at')
    search_fields = ('title',)

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('fact', 'name')
    search_fields = ('name',)

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('group', 'name')
    search_fields = ('name',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text',)
    search_fields = ('text',)

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('fact', 'question', 'group', 'member', 'score')
    search_fields = ('fact__title', 'question__text', 'member__name')
