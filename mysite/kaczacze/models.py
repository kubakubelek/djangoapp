from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
# Create your models here.

class Wpis(models.Model):
    content=models.TextField()
    date=models.DateField(default=timezone.now)
    time=models.CharField(max_length=100, null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    status = models.CharField(default='make_post', max_length=100)
    def __str__(self):
        return self.content

class Komentarz(models.Model):
    wpis=models.ForeignKey('Wpis',on_delete=models.CASCADE, related_name='komentarze')
    content=models.CharField(max_length=300)
    date=models.DateField(default=timezone.now)
    time=models.CharField(max_length=100, null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE, default=1)
    status = models.CharField(default='comment_post', max_length=100)
    def __str__(self):
        return self.content

class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    image=models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics')
    bio=models.TextField(default='')
    def __str__(self):
       return f'{self.user.username} Profile'