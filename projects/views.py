from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework.response import Response
from myapp.permissons import IsOwnerOnly
from .forms import ProjectForm, AddMemberForm
from myapp.forms import FolderForm
from django.contrib.auth.models import User
from myapp.models import Folder
from .models import Project, ProjectMember
from django.shortcuts import get_object_or_404
from .serializers import ProjectSerializer
from rest_framework import generics


@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            project.members.add(request.user)

            messages.success(request, 'New project has been created!')
            return redirect('project-list')
    else:
        form = ProjectForm()

    projects = Project.objects.filter(user=request.user)
    return render(request, 'create_project.html', {'form': form, 'projects': projects})


@login_required
def delete_project(request, pk):
    project = Project.objects.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('project-list')
    return render(request, 'delete_task.html', {'obj': project})


@login_required
def project_list(request):
    projects = Project.objects.filter(user=request.user)
    return render(request, 'projects.html', {'projects': projects})


@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    folders = Folder.objects.filter(project=project)
    members = ProjectMember.objects.filter(project=project)

    context = {
        'project': project,
        'folders': folders,
        'members': members,
    }

    return render(request, 'project_detail.html', context)


@login_required
def update_project(request, pk):
    project = Project.objects.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'project_form.html', context)


@login_required
def add_member(request, project_id):
    project = Project.objects.get(id=project_id)

    if request.method == 'POST':
        form = AddMemberForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                user = User.objects.get(username=username)
                if not project.members.filter(id=user.id).exists():
                    project.members.add(user)
                    user.projects.add(project)
                    messages.success(request, f'User {user.username} has been added to the project.')
                else:
                    messages.warning(request, f'User {user.username} is already a member of the project.')
            except User.DoesNotExist:
                messages.error(request, f'User with username {username} does not exist.')
    else:
        form = AddMemberForm()

    return render(request, 'add_member.html', {'form': form})


@login_required
def createfolderp(request, project_id):
    if request.method == 'POST':
        folder_form = FolderForm(request.POST)
        if folder_form.is_valid():

            folder = folder_form.save(commit=False)
            folder.project = Project.objects.get(id=project_id)
            folder.save()

            return redirect('project-detail', project_id)
    else:
        folder_form = FolderForm()

    return render(request, 'create_folderp.html', {'folder_form': folder_form})


class ProjectAPIList(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = (IsOwnerOnly,)

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProjectAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = (IsOwnerOnly, )

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)
