from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm, LoginForm, TaskForm
from .models import Task
from django.contrib.auth.decorators import login_required
from datetime import datetime

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
    date_filter = request.GET.get('date')
    if date_filter:
        date = datetime.strptime(date_filter, '%Y-%m-%d').date()
        tasks = Task.objects.filter(user=request.user, start_date_lte=date, end_date_gte=date)
    else:
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