from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, Folder
from .forms import ProjectForm, FolderForm
import os
from django.db.models import Q

from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib.auth.models import User
from store.models import User
from store.forms import UserForm
from .forms import UserRegistrationForm, UserUpdateForm


@login_required
def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'register_user.html', {'form': form})

# Log out view

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout


@login_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})


@login_required
def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'user_detail.html', {'user': user})

@login_required
def update_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')  # Redirect to the user list view
    else:
        form = UserForm(instance=user)
    return render(request, 'update_user.html', {'form': form, 'user': user})

@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('user_list')  # Redirect to the user list view

# Landing page view
@login_required
def landing_page(request):
    # Retrieve the current user's department
    department = request.user.department

    # Filter projects based on the user's department
    projects = Project.objects.filter(department=department)

    return render(request, 'base.html', {'projects': projects})


@login_required
def code_department_projects(request):
    if request.user.department == 'code':
        # Fetch code department projects
        projects = Project.objects.filter(department='code', user=request.user)
        return render(request, 'code.html', {'projects': projects})
    else:
        raise Http404("Page not found.")

@login_required
def document_department_projects(request):
    if request.user.department == 'document':
        # Fetch document department projects
        projects = Project.objects.filter(department='document', user=request.user)
        return render(request, 'document.html', {'projects': projects})
    else:
        raise Http404("Page not found.")

    
# Create project view
@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user  # Assuming you have implemented user authentication

            # Ensure that the selected department matches the user's department
            if project.user.department == project.department:
                project.save()

                # Determine the appropriate redirect URL based on the user's department
                if project.department == 'code':
                    return redirect('code_department_projects')
                elif project.department == 'document':
                    return redirect('document_department_projects')
                else:
                    return redirect('project_list')

            else:
                # Display an error message if the selected department is different from the user's department
                form.add_error('department', "You can only select your own department.")
    else:
        form = ProjectForm(initial={'department': request.user.department})  # Set the initial value for the department field to the user's department

    return render(request, 'create_project.html', {'form': form})

# Project list view
@login_required
def project_list(request):
    if request.user.department == 'code':
        return redirect('code_department_projects')  # Redirect to the code department project list
    elif request.user.department == 'document':
        return redirect('document_department_projects')  # Redirect to the document department project list
    else:
        department = request.GET.get('department')
        query = request.GET.get('query')
        if department:
            projects = Project.objects.filter(department=department)
            if query:
                projects = projects.filter(
                    Q(title__icontains=query) | Q(description__icontains=query)
                )
        else:
            projects = Project.objects.all()
            if query:
                projects = projects.filter(
                    Q(title__icontains=query) | Q(description__icontains=query)
                )

        total_projects = projects.count()
        return render(request, 'project_list.html', {'projects': projects, 'total_projects': total_projects})

# Project detail view

@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    folders = Folder.objects.filter(project=project)
    return render(request, 'project_detail.html', {'project': project, 'folders': folders})

# Update project view

@login_required
def update_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_detail', project_id=project_id)  # Redirect to the project detail view
    else:
        form = ProjectForm(instance=project)
    return render(request, 'update_project.html', {'form': form, 'project': project})

# Delete project view

@login_required
def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        project.delete()
        return redirect('project_list')  # Redirect to the project list view
    return render(request, 'delete_project.html', {'project': project})

# Create folder view

@login_required
def create_folder(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        form = FolderForm(request.POST, request.FILES)
        if form.is_valid():
            folder = form.save(commit=False)
            folder.project = project
            folder.save()
            return redirect('project_detail', project_id=project_id)  # Redirect to the project detail view
    else:
        form = FolderForm()
    return render(request, 'create_folder.html', {'form': form, 'project': project})

# Folder list view

@login_required
def folder_list(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    folders = Folder.objects.filter(project=project)
    return render(request, 'folder_list.html', {'project': project, 'folders': folders})

# Folder detail view

@login_required
def folder_detail(request, project_id, folder_id):
    folder = get_object_or_404(Folder, pk=folder_id, project_id=project_id)
    return render(request, 'folder_detail.html', {'folder': folder})

# Update folder view

@login_required
def update_folder(request, project_id, folder_id):
    folder = get_object_or_404(Folder, pk=folder_id, project_id=project_id)
    if request.method == 'POST':
        form = FolderForm(request.POST, request.FILES, instance=folder)
        if form.is_valid():
            form.save()
            return redirect('folder_detail', project_id=project_id, folder_id=folder_id)  # Redirect to the folder detail view
    else:
        form = FolderForm(instance=folder)
    return render(request, 'update_folder.html', {'form': form, 'folder': folder})

# Delete folder view

@login_required
def delete_folder(request, project_id, folder_id):
    folder = get_object_or_404(Folder, pk=folder_id, project_id=project_id)
    if request.method == 'POST':
        folder.delete()
        return redirect('project_detail', project_id=project_id)  # Redirect to the project detail view
    return render(request, 'delete_folder.html', {'folder': folder})

# Download folder view

@login_required
def download_folder(request, folder_id):
    folder = get_object_or_404(Folder, pk=folder_id)
    folder_path = os.path.join(settings.MEDIA_ROOT, str(folder.folder))
    filename = os.path.basename(folder_path)
    with open(folder_path, 'rb') as f:
        response = HttpResponse(f, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
