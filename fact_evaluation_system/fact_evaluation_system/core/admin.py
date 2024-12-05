from django.contrib import admin

from django.contrib import admin
from .models import User, Course, FACT, Criterion, Evaluation, Enrollment

admin.site.register(User)
admin.site.register(Course)
admin.site.register(FACT)
admin.site.register(Criterion)
admin.site.register(Evaluation)
admin.site.register(Enrollment)
