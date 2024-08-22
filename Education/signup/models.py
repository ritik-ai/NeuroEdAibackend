from django.db import models

# Create your models here.



class users(models.Model):
    Name = models.CharField(max_length=100),
    Email = models.EmailField(max_length=100),
    Password = models.CharField(max_length=100),
    country = models.CharField(max_length=50),
    