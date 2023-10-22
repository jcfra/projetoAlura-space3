from django.shortcuts import render, redirect
from django.contrib.auth.models import User #importa o model User
from django.contrib import auth #importa o pacote de autenticação do django
from usuarios.forms import LoginForms, CadastroForms
from django.contrib import messages

def login(request):
    form = LoginForms(request.POST)

    if form.is_valid():
       nome = form['nome_login'].value()
       senha = form['senha'].value()
       usuario = auth.authenticate(
            request,
            username=nome,
            password=senha)
       if usuario is not None:
          auth.login(request, usuario)
          messages.success(request, f'{nome} : Login realizado com sucesso!')
          return redirect ('index')
       else:
            messages.error(request, 'Erro ao efetuar login')
            return redirect('login')  
    return render(request, 'usuarios/login.html', {'form': form})

def cadastro(request):
    if not (request.user.is_authenticated):
        messages.error(request, 'Você precisa estar logado para cadastrar um usuário!')
        return redirect('login')
    form = CadastroForms()
    if request.method == 'POST':
        form = CadastroForms(request.POST)
        if form.is_valid():
            if form["senha_1"].value() != form["senha_2"].value():
                messages.error(request, 'Senhas não são iguais!')
                return redirect ('cadastro')
            nome=form['nome_cadastro'].value()
            email=form['email'].value()
            senha=form['senha_1'].value()
            if User.objects.filter(username=nome).exists():
                messages.error(request, 'Usuário já existe!')
                return redirect('cadastro')

            usuario = User.objects.create_user(
                username=nome,
                email=email,
                password=senha
            )
            usuario.save()
            messages.success(request, f'{nome} : Usuário cadastrado com sucesso!')
            return redirect('login')
    return render(request, 'usuarios/cadastro.html', {'form': form})

def logout(request):
    auth.logout(request)
    messages.success(request, 'Logout realizado com sucesso!')
    return redirect('login')