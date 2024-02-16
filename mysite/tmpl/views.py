from django.shortcuts import render
from django.views import View
# Create your views here.

class GameView(View):
    def get(self,request,guess):

        try:
            guess = int(guess)
            is_integer = True
        except ValueError:
            is_integer = False
        x={'guess': guess, 'is_integer': is_integer}
        return render(request, 'tmpl/main.html',x)