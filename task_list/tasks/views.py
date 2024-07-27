from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
from .models import Task

# Página index
@login_required
def index(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'tasks/index.html', {'tasks': tasks})

# Página para adicionar Tasks
def add_task(request):
    if request.method == 'POST':
        title = request.POST['title']
        Task.objects.create(title=title, user=request.user)
        return redirect('index')
    return render(request, 'tasks/add_task.html')

# Botão para excluir tasks
@login_required
def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.delete()
    return redirect('index')

# Criação da página de Cadastro e Login
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'tasks/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'tasks/login.html', {'form': form})

# Botão para editar as tasks
from django.shortcuts import render, redirect, get_object_or_404
from .forms import TaskForm

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/edit_task.html', {'form': form})

# Tasks Completas
@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = True
    task.save()
    return redirect('index')