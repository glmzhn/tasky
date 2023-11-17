from django import forms
from .models import Task, Folder


class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['name']


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        exclude = ('is_completed', 'created', 'user', 'folder')
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class TaskSearchForm(forms.Form):
    search = forms.CharField(max_length=100, label='Поиск')
