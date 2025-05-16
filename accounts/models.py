from django.db import models

class account(models.Model):
    username = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    password = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    
# Create your models here.
