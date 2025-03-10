from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string


class User(AbstractUser):
    isVerified = models.BooleanField(default=False)
    VerificationCode = models.CharField(max_length=255, default="")
    accessCode = models.CharField(max_length=255, default="", blank=True)
    
    def regenerate_access_code(self):
        """Generate a new random access code."""
        self.accessCode = get_random_string(length=50)  # Adjust length as needed
        self.save()

class Project(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/', blank=True)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    projectSubThemes = models.JSONField(default=list, blank=True)
    image_base64 = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=255)
    Image = models.ImageField(upload_to='images/', blank=True)
    File = models.FileField(upload_to='pdfs/')
    content = models.TextField()
    description = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    projects = models.ManyToManyField(Project, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    image_base64 = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title
    


# Create your models here.
