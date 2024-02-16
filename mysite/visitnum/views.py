from django.shortcuts import render
from datetime import datetime
from django.views import View
import base64
# Create your views her
class Main(View):
    def get(self, request):
        currentdate=datetime.now().strftime('%y-%m-%d')
        if 'date' not in request.session:
            request.session['date']=currentdate
        else:
            if request.session['date']!=currentdate:
                request.session['date']=currentdate
                del request.session['numvisit']
        try:
            numvisit=int(request.session.get('numvisit'))+1
        except:
            numvisit=1
        request.session['numvisit']=numvisit

        return render(request,'visitnum/main.html',{'numvisit': request.session['numvisit']})