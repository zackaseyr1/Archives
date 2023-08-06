from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    DEPARTMENT_CHOICES = [
        ('code', 'Code'),
        ('document', 'Document'),
        ('admin', 'Admin'),
    ]

    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES)
    block = models.BooleanField(default=False)


    def __str__(self):
        return self.username
    
    class Meta:
        app_label = 'store'

class Project(models.Model):
    DEPARTMENT_CHOICES = [
        ('document', 'Document'),
        ('code', 'Code'),
    ]

    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES)
    title = models.CharField(max_length=100)
    description = RichTextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Folder(models.Model):
    title = models.CharField(max_length=100)
    description = RichTextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    folder = models.FileField(upload_to='folders/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
