from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone
from .forms import UserRegistrationForm
from .models import User, Course, Enrollment, FACT, Criterion, Evaluation
from django.db.models import Avg


def home(request):
    return render(request, 'core/home.html')



def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.user_type == 'professor':
                return redirect('professor_dashboard')
            else:
                return redirect('student_dashboard')
        else:
            messages.error(request, 'Credenciais inválidas.')
    return render(request, 'core/login.html')

def user_logout(request):
    logout(request)
    return redirect('home')

from django.contrib.auth.decorators import login_required
from .models import Course, Enrollment, FACT

@login_required
def professor_dashboard(request):
    if request.user.user_type != 'professor':
        return redirect('home')
    courses = Course.objects.filter(professors=request.user)
    return render(request, 'core/professor_dashboard.html', {'courses': courses})

@login_required
def professor_course_detail(request, course_id):
    if request.user.user_type != 'professor':
        return redirect('home')
    course = get_object_or_404(Course, id=course_id, professors=request.user)
    students = Enrollment.objects.filter(course=course)
    facts = FACT.objects.filter(course=course)
    return render(request, 'core/professor_course_detail.html', {
        'course': course,
        'students': students,
        'facts': facts,
    })


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Enrollment, FACT

@login_required
def student_dashboard(request):
    if request.user.user_type != 'student':
        return redirect('home')
    
    # Obter as matrículas do aluno
    enrollments = Enrollment.objects.filter(student=request.user)
    courses = [enrollment.course for enrollment in enrollments]
    
    # Obter os FACTs ativos (com prazo ainda não expirado)
    active_facts = FACT.objects.filter(course__in=courses, is_active=True, deadline__gt=timezone.now())
    
    # Obter os FACTs cujo prazo já expirou
    completed_facts = FACT.objects.filter(course__in=courses, deadline__lte=timezone.now())
    
    # Calcular as notas dos FACTs concluídos
    # Obter os FACTs cujo prazo já expirou
    completed_facts = FACT.objects.filter(course__in=courses, deadline__lte=timezone.now())

    # Calcular as notas dos FACTs concluídos
    fact_scores = {}
    for fact in completed_facts:
        # Verificar se o aluno respondeu ao FACT
        responded = Evaluation.objects.filter(fact=fact, evaluator=request.user).exists()
        
        if responded:
            # O aluno respondeu ao FACT
            # Obter as avaliações recebidas pelo aluno neste FACT
            evaluations = Evaluation.objects.filter(fact=fact, evaluated=request.user)
            
            if evaluations.exists():
                # Número de pessoas que avaliaram o aluno (excluindo aqueles que não responderam)
                responded_students_ids = Evaluation.objects.filter(fact=fact).values_list('evaluator', flat=True).distinct()
                responded_students = User.objects.filter(id__in=responded_students_ids)
                
                num_evaluators = evaluations.values('evaluator').filter(evaluator__in=responded_students).distinct().count()
                
                # Soma das médias dos critérios de cada avaliação recebida
                total_average_score = 0
                
                # Agrupar as avaliações por avaliador
                evaluators = evaluations.values('evaluator').filter(evaluator__in=responded_students).distinct()
                
                for evaluator in evaluators:
                    evaluator_id = evaluator['evaluator']
                    # Obter as avaliações deste avaliador para o aluno
                    evaluator_evaluations = evaluations.filter(evaluator__id=evaluator_id)
                    
                    # Calcular a média dos critérios nesta avaliação
                    average_score = evaluator_evaluations.aggregate(avg_score=Avg('score'))['avg_score']
                    total_average_score += average_score
                
                # Calcular a nota final do aluno
                if num_evaluators > 0:
                    final_score = total_average_score / num_evaluators
                else:
                    final_score = 0  # Se nenhum avaliador válido, nota zero
            else:
                final_score = 0  # Nenhuma avaliação recebida, nota zero
        else:
            # O aluno não respondeu ao FACT, nota zero
            final_score = 0
        
        fact_scores[fact] = final_score


@login_required
def student_dashboard(request):
    if request.user.user_type != 'student':
        return redirect('home')

    # Obter as matrículas do aluno
    enrollments = Enrollment.objects.filter(student=request.user)
    courses = [enrollment.course for enrollment in enrollments]

    # Verificar se o aluno está matriculado em algum curso
    if not courses:
        messages.info(request, 'Você não está matriculado em nenhum curso.')
        return render(request, 'core/student_dashboard.html', {
            'active_facts': [],
            'fact_scores': {},
        })

    # Obter os FACTs ativos (com prazo ainda não expirado)
    active_facts = FACT.objects.filter(course__in=courses, is_active=True, deadline__gt=timezone.now())

    # Obter os FACTs cujo prazo já expirou
    completed_facts = FACT.objects.filter(course__in=courses, deadline__lte=timezone.now())

    # Calcular as notas dos FACTs concluídos
    fact_scores = {}
    for fact in completed_facts:
        # Verificar se o aluno respondeu ao FACT
        responded = Evaluation.objects.filter(fact=fact, evaluator=request.user).exists()

        if responded:
            # O aluno respondeu ao FACT
            # Obter as avaliações recebidas pelo aluno neste FACT
            evaluations = Evaluation.objects.filter(fact=fact, evaluated=request.user)

            if evaluations.exists():
                # Obter os alunos que responderam ao FACT
                responded_students_ids = Evaluation.objects.filter(fact=fact).values_list('evaluator', flat=True).distinct()
                responded_students = User.objects.filter(id__in=responded_students_ids)

                num_evaluators = evaluations.values('evaluator').filter(evaluator__in=responded_students).distinct().count()

                # Soma das médias dos critérios de cada avaliação recebida
                total_average_score = 0

                # Agrupar as avaliações por avaliador
                evaluators = evaluations.values('evaluator').filter(evaluator__in=responded_students).distinct()

                for evaluator in evaluators:
                    evaluator_id = evaluator['evaluator']
                    # Obter as avaliações deste avaliador para o aluno
                    evaluator_evaluations = evaluations.filter(evaluator__id=evaluator_id)

                    # Calcular a média dos critérios nesta avaliação
                    average_score = evaluator_evaluations.aggregate(avg_score=Avg('score'))['avg_score']
                    total_average_score += average_score

                # Calcular a nota final do aluno
                if num_evaluators > 0:
                    final_score = total_average_score / num_evaluators
                else:
                    final_score = 0  # Se nenhum avaliador válido, nota zero
            else:
                final_score = 0  # Nenhuma avaliação recebida, nota zero
        else:
            # O aluno não respondeu ao FACT, nota zero
            final_score = 0

        fact_scores[fact] = final_score

    # Renderizar o template com o contexto adequado
    return render(request, 'core/student_dashboard.html', {
        'request': request,
        'active_facts': active_facts,
        'fact_scores': fact_scores,
    })



from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib import messages

@login_required
def create_fact(request, course_id):
    if request.user.user_type != 'professor':
        return redirect('home')
    course = get_object_or_404(Course, id=course_id, professors=request.user)
    if request.method == 'POST':
        description = request.POST.get('description')
        deadline_str = request.POST.get('deadline')
        criteria_ids = request.POST.getlist('criteria')
        # Converter a string de deadline para datetime
        from datetime import datetime
        deadline = datetime.strptime(deadline_str, '%Y-%m-%dT%H:%M')
        criteria = Criterion.objects.filter(id__in=criteria_ids)
        # Criar o FACT
        fact = FACT.objects.create(
            course=course,
            deadline=deadline,
            description=description,
            is_active=True
        )
        fact.criteria.set(criteria)
        fact.save()
        messages.success(request, 'FACT criado com sucesso!')
        return redirect('professor_course_detail', course_id=course.id)
    else:
        criteria = Criterion.objects.all()
    return render(request, 'core/create_fact.html', {'course': course, 'criteria': criteria})



import matplotlib.pyplot as plt
import io
import urllib, base64

@login_required
def fact_results(request, fact_id):
    if request.user.user_type != 'professor':
        return redirect('home')
    fact = FACT.objects.get(id=fact_id)
    evaluations = Evaluation.objects.filter(fact=fact)
    criteria = fact.criteria.all()
    criteria_names = [c.name for c in criteria]
    averages = []
    for criterion in criteria:
        scores = evaluations.filter(criterion=criterion).values_list('score', flat=True)
        averages.append(sum(scores)/len(scores))
    # Gerar o gráfico
    plt.bar(criteria_names, averages)
    plt.xlabel('Critérios')
    plt.ylabel('Média da Turma')
    plt.title('Resultados do FACT')
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return render(request, 'core/fact_results.html', {'data': uri})


from django.db.models import Sum, Avg

@login_required
def fact_evaluations(request, fact_id):
    if request.user.user_type != 'professor':
        return redirect('home')
    
    try:
        fact = FACT.objects.get(id=fact_id)
    except FACT.DoesNotExist:
        messages.error(request, 'O FACT não foi encontrado.')
        return redirect('professor_dashboard')
    
    # Verificar se o professor está associado ao curso do FACT
    if request.user not in fact.course.professors.all():
        messages.error(request, 'Você não tem permissão para visualizar este FACT.')
        return redirect('professor_dashboard')
    
    # Obter todos os alunos matriculados no curso
    enrollments = Enrollment.objects.filter(course=fact.course)
    students = [enrollment.student for enrollment in enrollments]
    
    # Obter os critérios do FACT
    criteria = fact.criteria.all()
    
    # Verificar se há alunos matriculados
    if not students:
        messages.error(request, 'Não há alunos matriculados neste curso.')
        return redirect('professor_dashboard')
    
    # Preparar um dicionário para armazenar as notas dos alunos
    student_scores = {}
    
    for student in students:
        # Obter todas as avaliações recebidas pelo aluno neste FACT
        evaluations = Evaluation.objects.filter(fact=fact, evaluated=student)
        
        if evaluations.exists():
            # Número de pessoas que avaliaram o aluno (excluindo aqueles que não responderam)
            responded_students_ids = Evaluation.objects.filter(fact=fact).values_list('evaluator', flat=True).distinct()
            responded_students = User.objects.filter(id__in=responded_students_ids)
            
            num_evaluators = evaluations.values('evaluator').filter(evaluator__in=responded_students).distinct().count()
            
            # Soma das médias dos critérios de cada avaliação recebida
            total_average_score = 0
            
            # Agrupar as avaliações por avaliador
            evaluators = evaluations.values('evaluator').filter(evaluator__in=responded_students).distinct()
            
            for evaluator in evaluators:
                evaluator_id = evaluator['evaluator']
                # Obter as avaliações deste avaliador para o aluno
                evaluator_evaluations = evaluations.filter(evaluator__id=evaluator_id)
                
                # Calcular a média dos critérios nesta avaliação
                average_score = evaluator_evaluations.aggregate(avg_score=Avg('score'))['avg_score']
                total_average_score += average_score
            
            # Calcular a nota final do aluno
            if num_evaluators > 0:
                final_score = total_average_score / num_evaluators
            else:
                final_score = 0  # Se nenhum avaliador válido, nota zero
        else:
            final_score = 0  # Nenhuma avaliação recebida, nota zero
        
        # Armazenar a nota do aluno
        student_scores[student] = final_score
    
    context = {
        'fact': fact,
        'criteria': criteria,
        'student_scores': student_scores,
    }
    return render(request, 'core/fact_evaluations.html', context)




@login_required
def student_evaluations_detail(request, fact_id, student_id):
    if request.user.user_type != 'professor':
        return redirect('home')
    
    fact = get_object_or_404(FACT, id=fact_id)
    student = get_object_or_404(User, id=student_id, user_type='student')
    
    # Verificar se o professor está associado ao curso do FACT
    if request.user not in fact.course.professors.all():
        messages.error(request, 'Você não tem permissão para visualizar este FACT.')
        return redirect('professor_dashboard')
    
    # Obter todas as avaliações recebidas pelo aluno neste FACT
    evaluations = Evaluation.objects.filter(fact=fact, evaluated=student)
    
    # Agrupar avaliações por avaliador e obter o comentário uma vez
    evaluations_by_evaluator = {}
    evaluators = evaluations.values('evaluator').distinct()
    for evaluator in evaluators:
        evaluator_id = evaluator['evaluator']
        evaluator_user = User.objects.get(id=evaluator_id)
        evaluator_evaluations = evaluations.filter(evaluator__id=evaluator_id)
        # Obter o comentário de uma das avaliações
        comment = evaluator_evaluations.first().comment if evaluator_evaluations.exists() else ''
        evaluations_by_evaluator[evaluator_user] = {
            'evaluations': evaluator_evaluations,
            'comment': comment,
        }
    
    context = {
        'fact': fact,
        'student': student,
        'evaluations_by_evaluator': evaluations_by_evaluator,
    }
    return render(request, 'core/student_evaluations_detail.html', context)

@login_required
def respond_fact(request, fact_id):
    if request.user.user_type != 'student':
        return redirect('home')
    
    fact = get_object_or_404(FACT, id=fact_id, is_active=True)
    
    # Verificar se o prazo do FACT já expirou
    if fact.deadline < timezone.now():
        messages.error(request, 'O prazo para responder a este FACT já expirou.')
        return redirect('student_dashboard')
    
    # Verificar se o aluno está matriculado no curso do FACT
    enrollment_exists = Enrollment.objects.filter(course=fact.course, student=request.user).exists()
    if not enrollment_exists:
        messages.error(request, 'Você não está matriculado neste curso.')
        return redirect('student_dashboard')
    
    # Verificar se o aluno já respondeu ao FACT
    already_responded = Evaluation.objects.filter(fact=fact, evaluator=request.user).exists()
    if already_responded:
        messages.info(request, 'Você já respondeu a este FACT.')
        return redirect('student_dashboard')
    
    if request.method == 'POST':
        # Obter os alunos da turma, excluindo o próprio usuário
        students = Enrollment.objects.filter(course=fact.course).exclude(student=request.user)
        criteria = fact.criteria.all()
        
        for student in students:
            student_id = student.student.id
            comment_key = f'comment_{student_id}'
            comment = request.POST.get(comment_key, '')
            
            for criterion in criteria:
                criterion_id = criterion.id
                score_key = f'score_{student_id}_{criterion_id}'
                score = request.POST.get(score_key)
                
                if score:
                    try:
                        score = int(score)
                        if 0 <= score <= 10:
                            Evaluation.objects.create(
                                fact=fact,
                                evaluator=request.user,
                                evaluated=student.student,
                                criterion=criterion,
                                score=score,
                                comment=comment if criterion == criteria.first() else ''
                            )
                        else:
                            messages.error(request, f"Pontuação inválida para {student.student.username} no critério {criterion.name}. As notas devem ser entre 0 e 10.")
                            return redirect('respond_fact', fact_id=fact.id)
                    except ValueError:
                        messages.error(request, f"Pontuação não é um número válido para {student.student.username} no critério {criterion.name}.")
                        return redirect('respond_fact', fact_id=fact.id)
                else:
                    messages.error(request, f"Você não atribuiu uma pontuação para {student.student.username} no critério {criterion.name}.")
                    return redirect('respond_fact', fact_id=fact.id)
        
        messages.success(request, 'Avaliação enviada com sucesso!')
        return redirect('student_dashboard')
    else:
        # Exibir o formulário de avaliação
        students = Enrollment.objects.filter(course=fact.course).exclude(student=request.user)
        criteria = fact.criteria.all()
        
        context = {
            'fact': fact,
            'students': [e.student for e in students],
            'criteria': criteria,
        }
        return render(request, 'core/respond_fact.html', context)
