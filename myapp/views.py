from django.shortcuts import render, redirect
from .forms import TaskForm, FolderForm
from .models import Task, Folder
from projects.models import Project
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import generics

from .permissons import IsAdminOnly, IsOwnerOnly
from .serializers import TaskSerializer, FolderSerializer
from rest_framework.permissions import IsAuthenticated


@login_required
def createtask(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']

            existing_task = Task.objects.filter(name=name, user=request.user).first()

            if not existing_task:
                task = form.save(commit=False)
                task.user = request.user
                task.save()

            else:
                messages.success(request, f"There's already the task named {name}!!!")

            return redirect('home')
    else:
        form = TaskForm()

    return render(request, 'create_task.html', {'form': form})


def home(request):
    user = request.user
    if user.is_authenticated:
        tasks = Task.objects.filter(user=user)
        context = {'tasks': tasks}
        return render(request, 'base.html', context)
    else:
        messages.success(request, 'You have to log in!')
        return redirect('login')


@login_required()
def task(request, pk):
    task = Task.objects.get(id=pk)
    context = {'task': task}
    return render(request, 'base.html', context)


@login_required
def deletetask(request, pk):
    task = Task.objects.get(id=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('home')
    return render(request, 'delete_task.html', {'obj': task})


@login_required
def updatetask(request, pk):
    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'task_form.html', context)


@login_required
def search_tasks(request):
    query = request.GET.get('q')
    if query is not None:
        tasks = Task.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        folders = Folder.objects.filter(name__icontains=query)
        projects = Project.objects.filter(name__icontains=query)
        tasks = tasks.select_related('folder')
    else:
        tasks = []
        folders = []
        projects = []

    context = {
        'tasks': tasks,
        'folders': folders,
        'projects': projects,
        'query': query,
    }
    return render(request, 'search_task.html', context)

@login_required
def profile(request):
    user = request.user

    context = {
        'user': user,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
    }
    return render(request, 'profile.html', context)


@login_required
def update_folder(request, pk):
    folder = Folder.objects.get(id=pk)
    form = TaskForm(instance=folder)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=folder)
        if form.is_valid():
            form.save()
            return redirect('folder-detail')

    context = {'form': form}
    return render(request, 'task_form.html', context)


@login_required
def folder_list(request):
    folders = Folder.objects.filter(user=request.user, project=None)
    return render(request, 'folder_list.html', {'folders': folders})


@login_required
def folder_detail(request, pk):
    folder = get_object_or_404(Folder, pk=pk)

    if request.method == 'POST':
        task_form = TaskForm(request.POST)
        if task_form.is_valid():
            task = task_form.save(commit=False)
            task.folder = folder
            task.save()
    elif 'delete_task' in request.POST:
        task_id = request.POST['task_id']
        Task.objects.filter(pk=task_id).delete()

    context = {
        'folder': folder,
        'task_form': TaskForm(),
    }
    return render(request, 'folder_detail.html', context)


@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)

    context = {
        'task': task,
    }

    return render(request, 'task_detail.html', context)


@login_required
def delete_folder(request, pk):
    folder = get_object_or_404(Folder, pk=pk)

    if request.method == 'POST':
        folder.delete()
        return redirect('folder-list')  # Перенаправляем на список папок после удаления

    context = {
        'folder': folder,
    }
    return render(request, 'delete_folder.html', context)


@login_required
def createtaskf(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id)

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.folder = folder
            task.save()
            return redirect('folder-detail', pk=folder_id)

    else:
        form = TaskForm()

        context = {
            'folder_id': folder_id,
            'form': form,
        }
        return render(request, 'create_task.html', context)


@login_required
def create_folder(request):
    if request.method == 'POST':
        form = FolderForm(request.POST)
        if form.is_valid():
            folder = form.save(commit=False)
            folder.user = request.user
            folder.save()
            return redirect('folder-list')

    else:
        form = FolderForm()

    context = {
        'form': form,
    }
    return render(request, 'create_folder.html', context)


class TaskAPIList(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = (IsOwnerOnly, )

    def get_queryset(self):
        user_tasks = Task.objects.filter(user=self.request.user, folder=None)
        folder_tasks = Task.objects.filter(folder__user=self.request.user)
        queryset = user_tasks | folder_tasks
        return queryset


class TaskAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = (IsOwnerOnly, )

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class FolderAPIList(generics.ListCreateAPIView):
    serializer_class = FolderSerializer
    permission_classes = (IsOwnerOnly,)

    def get_queryset(self):
        folders = Folder.objects.filter(user=self.request.user)
        project_folders = Folder.objects.filter(project__user=self.request.user)
        queryset = folders | project_folders
        return queryset


class FolderAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FolderSerializer
    permission_classes = (IsOwnerOnly, )

    def get_queryset(self):
        return Folder.objects.filter(user=self.request.user)
