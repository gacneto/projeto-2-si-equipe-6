from django.shortcuts import render, get_object_or_404, redirect
from .models import Fact, Group, Question, Response, Member
from django.utils import timezone

# View para a página inicial
def home(request):
    return render(request, 'fact/home.html')

# View para o professor criar um novo FACT
def create_fact(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        num_groups = int(request.POST['num_groups'])
        deadline = request.POST.get('deadline')  # Captura o prazo

        # Cria o FACT
        fact = Fact.objects.create(title=title, num_groups=num_groups, is_draft=True, deadline=deadline)

        for i in range(num_groups):
            num_members = int(request.POST.get(f'members_{i}', 0))
            group_name = f'Grupo {i + 1}'
            group = Group.objects.create(fact=fact, name=group_name)

            for j in range(num_members):
                member_name = request.POST.get(f'group_{i}_member_{j}')
                Member.objects.create(group=group, name=member_name)

        return redirect('fact_list')

    return render(request, 'fact/create_fact.html')

# View para listar FACTs (Professor)
def fact_list(request):
    facts = Fact.objects.all()
    return render(request, 'fact/fact_list.html', {'facts': facts})

# Detalhes do FACT
def fact_detail(request, fact_id):
    fact = get_object_or_404(Fact, id=fact_id)
    return render(request, 'fact/fact_detail.html', {'fact': fact})

# View para o professor visualizar respostas
def view_responses(request, fact_id):
    fact = get_object_or_404(Fact, id=fact_id)
    responses = Response.objects.filter(fact=fact).select_related('member', 'question', 'group')

    return render(request, 'fact/view_responses.html', {
        'fact': fact,
        'responses': responses
    })

# Publicar e deletar FACT
def post_fact(request, fact_id):
    fact = get_object_or_404(Fact, id=fact_id)
    fact.is_draft = False
    fact.save()
    return redirect('fact_list')

def delete_fact(request, fact_id):
    fact = get_object_or_404(Fact, id=fact_id)
    fact.delete()
    return redirect('fact_list')

# Listar FACTs disponíveis para o estudante
def fact_list_student(request):
    facts = Fact.objects.filter(is_draft=False)  # Apenas FACTs publicados
    return render(request, 'fact/fact_list_student.html', {
        'facts': facts,
        'now': timezone.now()  # Passando a data atual
    })

# Resolver um FACT
def resolve_fact(request, fact_id):
    fact = get_object_or_404(Fact, id=fact_id)

    # Verifica se o prazo expirou
    if fact.deadline and fact.deadline < timezone.now():
        return render(request, 'fact/submit_fact_response.html', {
            'fact': fact,
            'expired': True  # Variável para indicar que o prazo expirou
        })

    predefined_questions = Question.objects.all()  # Supondo que todas as perguntas sejam utilizadas
    return render(request, 'fact/submit_fact_response.html', {
        'fact': fact,
        'predefined_questions': predefined_questions,
    })

def submit_fact_response(request, fact_id):
    fact = get_object_or_404(Fact, id=fact_id)

    # Verifica se o prazo expirou
    if fact.deadline and fact.deadline < timezone.now():
        return render(request, 'fact/submit_fact_response.html', {
            'fact': fact,
            'expired': True  # Variável para indicar que o prazo expirou
        })

    # Mensagem de erro inicial
    error_message = None

    # Obtenha as perguntas pré-definidas do banco de dados
    predefined_questions = Question.objects.filter(
        text__in=[
            "Pensamento Crítico e Criatividade",
            "Comunicação",
            "Colaboração",
            "Qualidade das Entregas",
            "Presença",
            "Entregas e Prazos"
        ]
    )

    # Obtenha grupos e membros
    groups = fact.groups.all()
    members = {group.id: list(group.members.all()) for group in groups}
    selected_group_id = request.POST.get('selected_group')
    selected_group_members = members.get(int(selected_group_id), []) if selected_group_id else []

    # Obtenha IDs dos membros já avaliados para este FACT
    evaluated_member_ids = Response.objects.filter(fact=fact).values_list('member_id', flat=True)

    if request.method == "POST":
        selected_member_id = request.POST.get('selected_member')
        comment = request.POST.get('comment')  # Obtém o comentário do formulário

        if selected_group_id and selected_member_id:
            selected_member = get_object_or_404(Member, id=selected_member_id)

            # Verifique se o membro já foi avaliado
            if int(selected_member_id) in evaluated_member_ids:
                error_message = "Este integrante já foi avaliado."
            else:
                all_questions_answered = True
                responses_to_save = []

                # Processa as respostas para cada pergunta
                for question in predefined_questions:
                    score = request.POST.get(f"score_{question.id}")
                    if score is None:
                        all_questions_answered = False
                        break
                    responses_to_save.append(
                        Response(
                            fact=fact,
                            question=question,
                            group=Group.objects.get(id=selected_group_id),
                            member=selected_member,
                            score=int(score),
                            comment=comment  # Salva o comentário no Response
                        )
                    )

                # Se todas as perguntas foram respondidas, salva as respostas
                if all_questions_answered:
                    Response.objects.bulk_create(responses_to_save)

                    # Verifica se todos os membros foram avaliados
                    total_members = sum(len(group.members.all()) for group in groups)
                    evaluated_members = Response.objects.filter(fact=fact).values('member').distinct().count()

                    if evaluated_members == total_members:
                        fact.is_resolved = True
                        fact.save()

                    return redirect('fact_list_student')
                else:
                    error_message = "Por favor, responda todas as perguntas antes de enviar."

    return render(request, 'fact/submit_fact_response.html', {
        'fact': fact,
        'predefined_questions': predefined_questions,
        'groups': groups,
        'members': members,
        'selected_group_members': selected_group_members,
        'selected_group_id': selected_group_id,
        'error_message': error_message,
        'evaluated_member_ids': evaluated_member_ids  # Passa os IDs dos membros já avaliados
    })
