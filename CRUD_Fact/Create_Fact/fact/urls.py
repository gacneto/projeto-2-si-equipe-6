from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_fact, name='create_fact'),
    path('list/', views.fact_list, name='fact_list'),
    path('post/<int:fact_id>/', views.post_fact, name='post_fact'),
    path('delete/<int:fact_id>/', views.delete_fact, name='delete_fact'),
    path('student/', views.fact_list_student, name='fact_list_student'),
    path('submit/<int:fact_id>/', views.submit_fact_response, name='submit_fact_response'),
    path('resolve/<int:fact_id>/', views.resolve_fact, name='resolve_fact'),  
    path('detail/<int:fact_id>/', views.fact_detail, name='fact_detail'),  
    path('responses/<int:fact_id>/', views.view_responses, name='view_responses'),
    path('grades/<int:fact_id>/', views.view_grades, name='view_grades'),
]
