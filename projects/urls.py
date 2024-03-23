from django.urls import path, include
from projects.views import ProjectAPIList, ProjectAPIDetailView
from . import views


urlpatterns = [
    path('project-list', views.project_list, name='project-list'),
    path('create-project', views.create_project, name='create-project'),
    path('delete-project/<int:pk>/', views.delete_project, name='delete-project'),
    path('project-detail/<int:project_id>/', views.project_detail, name='project-detail'),
    path('update-project/<int:pk>/', views.update_project, name='update-project'),
    path('add-member/<int:project_id>/', views.add_member, name='add-member'),
    path('create-folderp/<int:project_id>/', views.createfolderp, name='create-folderp'),
    path('api/v1/projects/', ProjectAPIList.as_view()),
    path('api/v1/projects/<int:pk>/', ProjectAPIDetailView.as_view())
]
