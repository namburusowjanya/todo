from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm, LoginForm, TaskForm
from .models import Task
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'todoapp/register.html', {'form': form})

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('task_list')
    else:
        form = LoginForm()
    return render(request, 'todoapp/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'todoapp/task_list.html', {'tasks': tasks})

@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'todoapp/add_task.html', {'form': form})

@login_required
def delete_task(request, task_id):
    Task.objects.get(id=task_id, user=request.user).delete()
    return redirect('task_list')

@login_required
@csrf_exempt
def update_task(request,task_id):
    task=Task.objects.get(id=task_id,user=request.user)
    if request.method=='POST':
        end_date=request.POST.get('end_date')
        completed=request.POST.get('completed')=='on'
        if end_date:
            try:
                task.end_date=datetime.strptime(end_date,'%y-%m-%d').date()
            except ValueError:
                pass
        task.completed=completed
        task.save()
    return redirect('task_list')