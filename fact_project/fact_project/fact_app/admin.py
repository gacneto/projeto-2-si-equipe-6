from django.contrib import admin

from django.contrib import admin
from .models import CustomUser, Course, Criterion, Fact, FactScore
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Course)
admin.site.register(Criterion)
admin.site.register(Fact)
admin.site.register(FactScore)
