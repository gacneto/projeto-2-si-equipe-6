from django.db import models
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import Course, Fact, FactScore, Criterion, CustomUser
from django.shortcuts import render

def teacher_home(request):
    return render(request, 'teacher_home.html')

def choose_role(request):
    return render(request, 'choose_role.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.role == 'teacher':
                return redirect('teacher_home')
            else:
                return redirect('student_home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def custom_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        role = request.POST.get('role')
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.role == role:
                login(request, user)
                if user.role == 'teacher':
                    return redirect('teacher_home')
                else:
                    return redirect('student_home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})



from django.contrib.auth.decorators import login_required

@login_required
def custom_logout(request):
    logout(request)
    return redirect('choose_role')


@login_required
def teacher_home(request):
    if request.user.role != 'teacher':
        return redirect('student_home')
    courses = Course.objects.all()
    return render(request, 'teacher_home.html', {'courses': courses})


@login_required
def course_detail(request, course_id):
    if request.user.role != 'teacher':
        return redirect('student_home')
    course = Course.objects.get(id=course_id)
    students = CustomUser.objects.filter(role='student')
    # Filtrar alunos por curso se necessário
    return render(request, 'course_detail.html', {'course': course, 'students': students})


@login_required
def student_home(request):
    if request.user.role != 'student':
        return redirect('teacher_home')
    return render(request, 'student_home.html')


@login_required
def cancel_fact(request):
    if request.user.role != 'student':
        return redirect('teacher_home')
    # Lógica para listar FACTs dentro do prazo
    return render(request, 'cancel_fact.html')


@login_required
def past_facts(request):
    if request.user.role != 'student':
        return redirect('teacher_home')
    facts = Fact.objects.filter(student=request.user)
    return render(request, 'past_facts.html', {'facts': facts})


################################


import matplotlib.pyplot as plt
import io
import urllib, base64
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Course, FactScore, Criterion, CustomUser

@login_required
def course_overview(request, course_id):
    if request.user.role != 'teacher':
        return redirect('student_home')

    course = Course.objects.get(id=course_id)
    criteria = Criterion.objects.all()
    students = CustomUser.objects.filter(role='student', course=course)

    # Calcula as médias por critério
    average_scores = []
    for criterion in criteria:
        scores = FactScore.objects.filter(
            criterion=criterion,
            fact__course=course,
            fact__student__in=students
        )
        if scores.exists():
            average = scores.aggregate(models.Avg('value'))['value__avg']
            average_scores.append(average)
        else:
            average_scores.append(0)

    # Gera o gráfico
    plt.figure(figsize=(10, 5))
    plt.bar([c.name for c in criteria], average_scores, color='blue')
    plt.xlabel('Critérios')
    plt.ylabel('Média das Notas')
    plt.title('Média por Critério')

    # Salva o gráfico em um buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    # Codifica a imagem em base64
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    context = {
        'course': course,
        'graphic': graphic,
    }

    return render(request, 'course_overview.html', context)
