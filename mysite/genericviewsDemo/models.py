from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class Country(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name
# Create your models here.
class Movies(models.Model):
    title=models.CharField(max_length=40)
    year=models.IntegerField(validators=[MinValueValidator(1875), MaxValueValidator(2027)])
    country=models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
