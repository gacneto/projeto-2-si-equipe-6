from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('professor/dashboard/', views.professor_dashboard, name='professor_dashboard'),
    path('professor/course/<int:course_id>/', views.professor_course_detail, name='professor_course_detail'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/fact/respond/<int:fact_id>/', views.respond_fact, name='respond_fact'),
    path('professor/course/<int:course_id>/create_fact/', views.create_fact, name='create_fact'),
    path('professor/fact/<int:fact_id>/results/', views.fact_evaluations, name='fact_evaluations'),
    path('professor/fact/<int:fact_id>/student/<int:student_id>/evaluations/', views.student_evaluations_detail, name='student_evaluations_detail'),
    # Outros caminhos para as funcionalidades
]
