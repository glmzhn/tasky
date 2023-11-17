from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tasks/<str:pk>/', views.task, name='task'),
    path('create-task', views.createtask, name='create-task'),
    path('create-task/<str:folder_id>/', views.createtaskf, name='create-taskf'),
    path('delete-task/<str:pk>/', views.deletetask, name='delete-task'),
    path('update-task/<str:pk>/', views.updatetask, name='update-task'),
    path('profile/', views.profile, name='profile'),
    path('search/', views.search_tasks, name='search-task'),
    path('create-folder/', views.create_folder, name='create-folder'),
    path('folders/', views.folder_list, name='folder-list'),
    path('folder/<str:pk>/', views.folder_detail, name='folder-detail'),
    path('update-folder/<str:pk>/', views.update_folder, name='update-folder'),
    path('delete-folder/<str:pk>/', views.delete_folder, name='delete-folder'),
    path('task/<str:pk>/', views.task_detail, name='task-detail'),
    path('contact/', views.contact, name='contact')
]
