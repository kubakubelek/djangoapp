from django.shortcuts import render
import random
# Create your views here.

def main(request):
    context={}

    if 'random_number' not in request.session:
        request.session['random_number']=random.randint(1,100)
    if 'countOfGuesses' not in request.session:
        request.session['countOfGuesses']=10


    if request.POST.get('guess'):
        user_guess=int(request.POST.get('guess'))
        random_num=request.session['random_number']
        count=request.session['countOfGuesses']

        request.session['countOfGuesses']=count-1
        context['count']=request.session['countOfGuesses']
        if  int(request.session['countOfGuesses'])==0:
            context['message']='You lose, Correct number was '+str(request.session['random_number'])
            del request.session['random_number']
            del request.session['countOfGuesses']
        else:
            if random_num>user_guess:
                context['message']='My number is bigger'
            elif random_num<user_guess:
                context['message']='My number is smaller'
            else:
                context['message']='You guessed'
                del request.session['random_number']
                del request.session['countOfGuesses']
    else:
        pass

    return render(request, 'numbergame/main.html',context)
