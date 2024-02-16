from django.db import models

# Create your models here.

class Movies(models.Model):
    title = models.CharField(max_length=255)
    year = models.IntegerField()
    genre=models.CharField(max_length=255)

