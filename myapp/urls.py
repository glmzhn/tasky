from django.urls import path, include, re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView, TokenRefreshView

from . import views
from myapp.views import TaskAPIList, TaskAPIDetailView, FolderAPIList, FolderAPIDetailView

urlpatterns = [
    path('', views.home, name='home'),
    path('tasks/<int:pk>/', views.task, name='task'),
    path('create-task/', views.createtask, name='create-task'),
    path('create-task/<int:folder_id>/', views.createtaskf, name='create-taskf'),
    path('delete-task/<int:pk>/', views.deletetask, name='delete-task'),
    path('update-task/<int:pk>/', views.updatetask, name='update-task'),
    path('profile/', views.profile, name='profile'),
    path('search/', views.search_tasks, name='search-task'),
    path('create-folder/', views.create_folder, name='create-folder'),
    path('folders/', views.folder_list, name='folder-list'),
    path('folder/<int:pk>/', views.folder_detail, name='folder-detail'),
    path('update-folder/<int:pk>/', views.update_folder, name='update-folder'),
    path('delete-folder/<int:pk>/', views.delete_folder, name='delete-folder'),
    path('task/<int:pk>/', views.task_detail, name='task-detail'),
    path('api/v1/tasks/', TaskAPIList.as_view()),
    path('api/v1/tasks/<int:pk>/', TaskAPIDetailView.as_view()),
    path('api/v1/folders/', FolderAPIList.as_view()),
    path('api/v1/folders/<int:pk>/', FolderAPIDetailView.as_view()),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
