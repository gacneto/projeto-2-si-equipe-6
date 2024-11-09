from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Usuario
from django.shortcuts import render

def escolha_usuario(request):
    return render(request, 'usuarios/escolha_usuario.html')

def login_docente(request):
    return render(request, 'usuarios/login_docente.html')

def menu(request):
    return render(request, 'usuarios/menu.html')

def login_aluno(request):
    return render(request, 'usuarios/login.html')


# def cadastro(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         matricula = request.POST.get('matricula')

#         if Usuario.objects.filter(email=email).exists():
#             messages.error(request, 'Este email já está cadastrado.')
#         elif Usuario.objects.filter(matricula=matricula).exists():
#             messages.error(request, 'Esta matrícula já está cadastrada.')
#         else:
#             novo_usuario = Usuario()
#             novo_usuario.nome = request.POST.get('nome')
#             novo_usuario.matricula = matricula
#             novo_usuario.email = email
#             novo_usuario.senha = request.POST.get('senha')
#             novo_usuario.save()
#             messages.success(request, 'Usuário cadastrado com sucesso!')

#         return render(request, 'usuarios/cadastro.html')

#     return render(request, 'usuarios/cadastro.html')

def cadastro(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        matricula = request.POST.get('matricula')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        if not email.endswith('@cesar.school'):
            messages.error(request, 'O email deve terminar com @cesar.school.')
            return redirect('cadastro')
        
        # Continue com o processamento do cadastro
        # Salvar no banco de dados, etc.

    return render(request, 'usuarios/cadastro.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        try:
            usuario = Usuario.objects.get(email=email, senha=senha)
            request.session['id_usuario'] = usuario.id_usuario
            messages.success(request, 'Login realizado com sucesso!')
            return redirect('dashboard')
        except Usuario.DoesNotExist:
            messages.error(request, 'Email ou senha incorretos.')
            return redirect('login')

    return render(request, 'usuarios/login.html')

def dashboard(request):
    if 'id_usuario' in request.session:
        usuario = Usuario.objects.get(id_usuario=request.session['id_usuario'])
        return render(request, 'usuarios/dashboard.html', {'usuario': usuario})
    else:
        return redirect('login')

def logout_view(request):
    if 'id_usuario' in request.session:
        del request.session['id_usuario']
    return redirect('login')


