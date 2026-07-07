from django.db import models
from django.contrib.auth.models import User

class Users(models.Model):
    username=models.CharField(max_length=20)
    password=models.CharField(max_length=20)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    bio = models.TextField(blank=True)
    newsletter = models.BooleanField(default=False)
    blog_posts = models.BooleanField(default=False)
    personal_offers = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    admin_reply = models.TextField(blank=True, null=True)
    replied_at = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return f"Message from {self.name}"
