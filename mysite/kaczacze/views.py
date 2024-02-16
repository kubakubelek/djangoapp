from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView, RedirectView, FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import WpisForm, KomentarzForm, BioForm
from .models import Wpis, Komentarz, Profile
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

class SignUp(CreateView):
    form_class=UserCreationForm
    template_name="registration/registration_form.html"
    def get_success_url(self):
        return reverse_lazy('login')
# Create your views here.

class PostDeleteView(DeleteView):
    model = Wpis

    def get_success_url(self):
        # Sprawdź, czy istnieje poprzednia strona (referer) w nagłówkach żądania HTTP
        if 'HTTP_REFERER' in self.request.META:
            return self.request.META['HTTP_REFERER']
        else:
            # Jeśli nie ma poprzedniej strony, użyj domyślnego success_url
            return reverse_lazy('main')

class CommentDeleteView(DeleteView):
    model=Komentarz
    def get_success_url(self):
        return self.request.META['HTTP_REFERER']

class ProfilePage(View):
    context={}
    def get(self,request, username):

        #username=request.GET['username']
        userP=User.objects.get(username=username)

        userposts=Wpis.objects.filter(user=userP).order_by('-id')
        self.context['userP']=userP
        self.context['userposts']=userposts
        self.context['form_komentarze'] = KomentarzForm()
        self.context['form_bio'] = BioForm(instance=userP)
        return render(request, 'kaczacze/user_profile.html', self.context)

class EditBio(View):

    def post(self,request, *args, **kwargs):
        profile=request.user.profile
        form = BioForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return JsonResponse({'bio': form.cleaned_data['bio']})
        else:
            return JsonResponse({'error': 'Invalid form data'}, status=400)



class WpisyListView(ListView,FormView):
    model = Wpis
    template_name = 'kaczacze/main.html'
    context_object_name = 'wpisy_list'
    form_class = WpisForm
    success_url = reverse_lazy('main')

    def get_queryset(self):
        # Pobieramy wszystkie obiekty Wpis i sortujemy je malejąco według daty
        return Wpis.objects.order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        wpisy = context['wpisy_list']
        context['form_komentarze'] = KomentarzForm()
        for wpis in wpisy:
            wpis.komentarze.set(wpis.komentarze.all())
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user  # Ustawienie autora postu
        current_date=timezone.now()
        time=str(timezone.now().hour+1).zfill(2)+':'+str(timezone.now().minute).zfill(2)

        post.time =time
        post.date=current_date
        post.save()
        return super().form_valid(form)

from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

class MyLoginView(LoginView):
    redirect_authenticated_user = True
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        # Pobierz parametr 'next' z żądania, jeśli istnieje
        next_url = self.request.POST.get('next')
        # Ustaw success_url na wartość parametru 'next', jeśli istnieje, w przeciwnym razie użyj wartości success_url zdefiniowanej powyżej
        self.success_url = next_url or self.success_url
        # Zwróć przekierowanie na success_url
        return HttpResponseRedirect(self.get_success_url())

#class MyLoginView(LoginView):
#    redirect_authenticated_user = True


class KomentarzCreateView(LoginRequiredMixin, CreateView):
    model = Komentarz
    fields = ['content']  # Pola, które mają być wyświetlane w formularzu

    def form_valid(self, form):
        post = form.save(commit=False)
        post.wpis = Wpis.objects.get(pk=self.kwargs.get('pk'))  # Poprawka
        post.user = self.request.user
        current_date = timezone.now()
        time = str(timezone.now().hour + 1).zfill(2) + ':' + str(timezone.now().minute).zfill(2)
        post.time = time
        post.date = current_date
        post.save()
        return super().form_valid(form)

    def get_success_url(self):
        # Użyj nagłówka HTTP_REFERER, aby przekierować użytkownika z powrotem do poprzedniej strony
        return self.request.META.get('HTTP_REFERER', '/kaczacze')



class Main(View):
    def get(self,request):

        form1 = WpisForm()
        form2 = KomentarzForm()

        context = {
        'form1': form1,
        'form2': form2,
        'wpis_list': Wpis.objects.all().order_by('-id')
        }



        return render(request, 'kaczacze/main.html', context)
    def post(self, request):
        form = WpisForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  # Ustawienie autora postu
            current_date=timezone.now()
            time=str(timezone.now().hour+1).zfill(2)+':'+str(timezone.now().minute).zfill(2)

            post.time =time
            post.date=current_date
            post.save()


        return redirect('main')

class SearchView(View):
    def post(self,request,query):
        return redirect('search', query=query)

    def get(self, request,query):


        context = {
        'form_komentarze':KomentarzForm(),
        'query':query,
        'users':User.objects.filter(username__icontains=query),
        'wpisy_list': Wpis.objects.all().filter(content__contains=query).order_by('-id')
        }
        return render(request, 'kaczacze/search.html', context)




