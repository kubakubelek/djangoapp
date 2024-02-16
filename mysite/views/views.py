from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.utils.html import escape
from django.views import View
import random
# Create your views here.

def danger(request):
    response="""<html><body><p>Your guess was """+request.GET['guess']+"""</p></body></html>"""
    return HttpResponse(response)

def game(request):
    response="""<html><body><p>Your guess was """+escape(request.GET['guess'])+"""</p></body></html>"""
    return HttpResponse(response)

class MainView(View):
    def get(self, request, guess=None):
        response="""<html><body><p>Your guess was """+escape(str(guess))+"""</p></body></html>"""
        return HttpResponse(response)

def bounce(request):
    return HttpResponseRedirect('https://kubakubelek.pythonanywhere.com/')

class BounceView(View):
    def get(self, request):
        number=random.randint(1,100)
        return HttpResponseRedirect('https://kubakubelek.pythonanywhere.com/views/main/'+str(number))