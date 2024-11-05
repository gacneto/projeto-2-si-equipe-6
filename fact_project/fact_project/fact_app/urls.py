from django.urls import path
from . import views

urlpatterns = [
    path('', views.choose_role, name='choose_role'),
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='custom_logout'),
    # Páginas do professor
    path('teacher/home/', views.teacher_home, name='teacher_home'),
    path('teacher/course/<int:course_id>/', views.course_detail, name='course_detail'),
    # Páginas do aluno
    path('student/home/', views.student_home, name='student_home'),
    path('student/cancel_fact/', views.cancel_fact, name='cancel_fact'),
    path('student/past_facts/', views.past_facts, name='past_facts'),
    # Outras rotas...
    path('teacher/course/<int:course_id>/overview/', views.course_overview, name='course_overview'),

]