from django.contrib import admin
from .models import Project, Folder, User

admin.site.register(Project)
admin.site.register(Folder)
admin.site.register(User)
