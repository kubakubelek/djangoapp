from django.db import models

# Create your models here.
class User(models.Model):
    nick=models.CharField(max_length=20, null=False)
    password=models.CharField(max_length=20, null=False)
    gender=models.CharField(max_length=100, null=False)
    birth_date=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    color=models.CharField(max_length=10)
