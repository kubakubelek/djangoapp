from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, TemplateView, RedirectView, FormView
from django.views.generic.list import ListView
from django.db.models.functions import Coalesce
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import WpisForm, KomentarzForm, BioForm, ProfilePictureForm
from .models import Wpis, Komentarz, Profile, Vote
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.db.models import Prefetch
from django.db.models import Sum, Value
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def upvote(request, pk):
    post = get_object_or_404(Wpis, pk=pk)





    # Check if the user has already voted on this post
    existing_vote = Vote.objects.filter(user=request.user, post=post).first()
    if not existing_vote:
        # If no vote exists, create a new vote
        Vote.objects.create(user=request.user, post=post, value=1)
    elif existing_vote.value == -1:
        # If the user downvoted before, change the vote to an upvote
        existing_vote.value = 1
        existing_vote.save()
    elif existing_vote.value == 1:
        # If the user downvoted before, change the vote to an upvote
        existing_vote.value = 0
        existing_vote.save()
    elif existing_vote.value == 0:
        # If the user downvoted before, change the vote to an upvote
        existing_vote.value = 1
        existing_vote.save()

     # Oblicz sumę głosów dla tego wpisu i zaktualizuj pole total_votes


    postToVote=Vote.objects.filter(post=post)
    votesum = postToVote.aggregate(Sum('value'))['value__sum']
    post.total_votes = votesum
    post.save()
    return JsonResponse({'success': True, 'VoteCount': votesum})



def downvote(request, pk):
    post = get_object_or_404(Wpis, pk=pk)
    # Check if the user has already voted on this post
    existing_vote = Vote.objects.filter(user=request.user, post=post).first()
    if not existing_vote:
        # If no vote exists, create a new vote
        Vote.objects.create(user=request.user, post=post, value=-1)
    elif existing_vote.value == 1:
        # If the user upvoted before, change the vote to a downvote
        existing_vote.value = -1
        existing_vote.save()
    elif existing_vote.value == -1:
        # If the user downvoted before, change the vote to an upvote
        existing_vote.value = 0
        existing_vote.save()
    elif existing_vote.value == 0:
        # If the user downvoted before, change the vote to an upvote
        existing_vote.value = -1
        existing_vote.save()

    postToVote=Vote.objects.filter(post=post)
    votesum = postToVote.aggregate(Sum('value'))['value__sum']
    post.total_votes = votesum
    post.save()
    return JsonResponse({'success': True, 'VoteCount': votesum})




class LikePost(View):
    def post(self, request, pk):
        post=get_object_or_404(Wpis, id=pk)
        post.likes.add(request.user)



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
    def post(self,request,username, *args, **kwargs):
        profile=request.user.profile
        form = ProfilePictureForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
        return redirect('profile' ,username=username)
    def get(self,request, username):
        vote_values={}
        for post in Wpis.objects.all():
        # Sprawdź, czy użytkownik zagłosował na ten post
            if self.request.user.is_authenticated:
                vote = Vote.objects.filter(user=self.request.user, post=post).first()

                # Jeśli użytkownik zagłosował na ten post, pobierz wartość głosu
                if vote:
                    vote_values[post.id] = vote.value
                else:
                    vote_values[post.id] = None
            else:
               vote_values[post.id] = 0
        #username=request.GET['username']
        userP=User.objects.get(username=username)

        userposts=Wpis.objects.filter(user=userP).order_by('-id')

        paginator = Paginator(userposts, 25)  # Show 25 contacts per page.

        page_number = self.request.GET.get("page")


        try:
            userposts = paginator.get_page(page_number)
        except PageNotAnInteger:
            # Jeśli numer strony nie jest liczbą całkowitą, pobierz pierwszą stronę
            userposts = paginator.get_page(1)
        except EmptyPage:
            # Jeśli numer strony nie istnieje, pobierz ostatnią stronę
            userposts = paginator.get_page(paginator.num_pages)





        self.context['userP']=userP
        self.context['vote_values']=vote_values
        self.context['userposts']=userposts
        self.context['form_komentarze'] = KomentarzForm()
        self.context['form_bio'] = BioForm(instance=userP)
        self.context['form_ProfilePicture']=ProfilePictureForm(instance=userP)
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
        queryset = super().get_queryset()
        #for post in queryset:
        #    postToVote=Vote.objects.filter(post=post)
        #    votesum = postToVote.aggregate(Sum('value'))['value__sum']
        #    post.total_votes = votesum or 0
        #postToVote=Vote.objects.filter(post=post)

        #queryset = queryset.annotate(total_votes=Sum('vote__value', default=0))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        wpisy = context['wpisy_list']





        context['form_komentarze'] = KomentarzForm()
        wpisy_z_komentarzami = Wpis.objects.prefetch_related(
        Prefetch('komentarze', queryset=Komentarz.objects.order_by('-id'))
        )
        #for post in wpisy_z_komentarzami:
        #    postToVote=Vote.objects.filter(post=post)
        #    votesum = postToVote.aggregate(Sum('value'))['value__sum']
        #    post.total_votes = votesum or 0

        option = self.request.GET.get('option')
        if option == 'most_liked':
            wpisy_z_komentarzami = wpisy_z_komentarzami.order_by('-total_votes')
        else:
            wpisy_z_komentarzami = wpisy_z_komentarzami.order_by('-id')

        paginator = Paginator(wpisy_z_komentarzami, 25)  # Show 25 contacts per page.

        page_number = self.request.GET.get("page")


        try:
            wpisy_z_komentarzami = paginator.get_page(page_number)
        except PageNotAnInteger:
            # Jeśli numer strony nie jest liczbą całkowitą, pobierz pierwszą stronę
            wpisy_z_komentarzami = paginator.get_page(1)
        except EmptyPage:
            # Jeśli numer strony nie istnieje, pobierz ostatnią stronę
            wpisy_z_komentarzami = paginator.get_page(paginator.num_pages)






        context["Vote"]=Vote.objects.all()
        vote_values={}
        for post in wpisy_z_komentarzami:
        # Sprawdź, czy użytkownik zagłosował na ten post
            if self.request.user.is_authenticated:
                vote = Vote.objects.filter(user=self.request.user, post=post).first()

                # Jeśli użytkownik zagłosował na ten post, pobierz wartość głosu
                if vote:
                    vote_values[post.id] = vote.value
                else:
                    vote_values[post.id] = None
            else:
               vote_values[post.id] = 0
        context['wpisy_list']=wpisy_z_komentarzami
        context['vote_values']=vote_values
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

from django.contrib.auth import logout

def custom_logout(request):
    logout(request)
    return redirect('/')

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
        vote_values={}
        for post in Wpis.objects.all():
        # Sprawdź, czy użytkownik zagłosował na ten post
            if self.request.user.is_authenticated:
                vote = Vote.objects.filter(user=self.request.user, post=post).first()

                # Jeśli użytkownik zagłosował na ten post, pobierz wartość głosu
                if vote:
                    vote_values[post.id] = vote.value
                else:
                    vote_values[post.id] = None
            else:
               vote_values[post.id] = 0


        context = {
        'vote_values':vote_values,
        'form_komentarze':KomentarzForm(),
        'query':query,
        'users':User.objects.filter(username__icontains=query),
        }
        wpisy_z_komentarzami=Wpis.objects.all().filter(content__contains=query).order_by('-id')
        paginator = Paginator(wpisy_z_komentarzami, 25)  # Show 25 contacts per page.

        page_number = self.request.GET.get("page")


        try:
            wpisy_z_komentarzami = paginator.get_page(page_number)
        except PageNotAnInteger:
            # Jeśli numer strony nie jest liczbą całkowitą, pobierz pierwszą stronę
            wpisy_z_komentarzami = paginator.get_page(1)
        except EmptyPage:
            # Jeśli numer strony nie istnieje, pobierz ostatnią stronę
            wpisy_z_komentarzami = paginator.get_page(paginator.num_pages)

        context['wpisy_list']=wpisy_z_komentarzami





        return render(request, 'kaczacze/search.html', context)




