from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from socialmedia.models import User
from django.views import View

# Create your views here.

class MainView(ListView):
    model=User

class LoginView(View):
    def get(self,request):
        return render(request,'socialmedia/login.html')

class RegisterView(View):
    def get(self,request):
        return render(request,'socialmedia/register.html')
    def post(self,request):
        context={}
        if User.objects.filter(nick=request.POST.get('nick')).exists():
            context['nick']="There is aalready someone whith this nick"
            return render(request,'socialmedia/register.html',context)
        else:
            new_user=User(nick=request.POST.get('nick'),password=request.POST.get('password'),gender=request.POST.get('gender'),birth_date=request.POST.get('birthday'),email=request.POST.get('email'),color=request.POST.get('color'))
            new_user.save()
            return redirect('list')