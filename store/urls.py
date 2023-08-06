from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
     #  Login
   # path('login/', views.login_view, name='login'),

     # Logout
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_user, name='register_user'),
    


    path('users/', views.user_list, name='user_list'),
   
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),
    path('users/<int:user_id>/update/', views.update_user, name='update_user'),
    path('users/<int:user_id>/delete/', views.delete_user, name='delete_user'),






    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    #path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),

    
    # Landing page
    path('', views.landing_page, name='landing_page'),
    path('projects/code/', views.code_department_projects, name='code_department_projects'),
    path('projects/document/', views.document_department_projects, name='document_department_projects'),
    # Create project
    path('create_project/', views.create_project, name='create_project'),

    # Project list
    path('project_list/', views.project_list, name='project_list'),

    # Project detail
    path('project_detail/<int:project_id>/', views.project_detail, name='project_detail'),

    # Update project
    path('update_project/<int:project_id>/', views.update_project, name='update_project'),

    # Delete project
    path('delete_project/<int:project_id>/', views.delete_project, name='delete_project'),

    # Create folder
    path('create_folder/<int:project_id>/', views.create_folder, name='create_folder'),

    # Folder list
    path('folder_list/<int:project_id>/', views.folder_list, name='folder_list'),

    # Folder detail
    path('folder_detail/<int:project_id>/<int:folder_id>/', views.folder_detail, name='folder_detail'),

    # Update folder
    path('update_folder/<int:project_id>/<int:folder_id>/', views.update_folder, name='update_folder'),

    # Delete folder
    path('delete_folder/<int:project_id>/<int:folder_id>/', views.delete_folder, name='delete_folder'),

    # Download folder
    path('folder/<int:folder_id>/download/', views.download_folder, name='download_folder'),


    
]

