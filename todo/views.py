from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from todo import models

from todo import forms


@login_required(login_url='loginUser')
def index(request):
    board_data = models.Board.objects.filter(owner=request.user)
    task_data = models.Task.objects.filter(board__owner=request.user)

    board_form = forms.BoardForm(request.POST or None)
    task_form = forms.TaskForm(request.POST or None)

    if request.method == 'POST':
        if 'create_board' in request.POST:
            if board_form.is_valid():
                broad_name = board_form.cleaned_data.get('name')
                board_data = models.Board.objects.create(name=broad_name)
                board_data.owner = request.user
                board_data.save()

        elif 'create_task' in request.POST:
            if task_form.is_valid():
                task_description = task_form.cleaned_data.get('description')
                board = models.Board.objects.get(
                    id=request.POST.get('create_task'))
                task_data = models.Task.objects.create(
                    description=task_description, board=board)
                task_data.save()

        elif 'complete' in request.POST:
            task = models.Task.objects.get(id=request.POST.get('complete'))
            task.completed = not task.completed
            task.save()

        elif 'close_board' in request.POST:

            board = get_object_or_404(
                models.Board, id=request.POST.get('close_board'))
            board.delete()

        elif 'close_task' in request.POST:

            task = get_object_or_404(
                models.Task, id=request.POST.get('close_task'))
            task.delete()

        return redirect('index')

    context = {
        'board_data': board_data,
        'task_data': task_data,
        'board_form': board_form,
        'task_form': task_form
    }

    return render(request, 'index.html', context)


@login_required(login_url='loginUser')
def update_board(request, id):
    instance = get_object_or_404(models.Board, id=id)
    board_form = forms.BoardForm(request.POST or None, instance=instance)
    if board_form.is_valid():
        board_form.save()
        return redirect('index')
    return render(request, 'update_board.html', {'board_form': board_form})


@login_required(login_url='loginUser')
def update_task(request, id):
    instance = get_object_or_404(models.Task, id=id)
    task_form = forms.TaskForm(request.POST or None, instance=instance)

    if task_form.is_valid():
        task_form.save()
        return redirect('index')
    return render(request, 'update_task.html', {'task_form': task_form})


def loginUser(request):
    form = forms.LoginForm(request.POST or None)

    context = {
        "form": form
    }
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, 'Username or Password is incorrect!')
            return render(request, 'login.html', context)

        login(request, user)
        return redirect('index')
    return render(request, 'login.html', context)


def register(request):
    form = forms.RegisterUserForm(request.POST or None)
    if form.is_valid():

        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        newUser = User(username=username)
        newUser.set_password(password)

        newUser.save()
        login(request, newUser)

        return redirect('index')

    context = {
        "form": form
    }
    return render(request, 'register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('index')
