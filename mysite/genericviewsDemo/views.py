from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from .forms import MovieForm
from genericviewsDemo.models import Movies, Country
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# Create your views here.


class SignUp(generic.edit.CreateView):
    form_class=UserCreationForm
    template_name="registration/registration_form.html"
    def get_success_url(self):
        return reverse_lazy('login')
    #sucess_url=reverse_lazy('login')

class MovieListView(generic.list.ListView):
    model = Movies


        #title=request.POST.get('title')
        #year=request.POST.get('year')
        #country=Country.objects.get(name=request.POST.get('country'))
        #object=Movies(title=title, year=year, country=country)
        #object.save()
        #return render(request, 'genericviewsDemo/movies_list.html', self.get_context())
        #return redirect(request.path)


class MovieDetailView(generic.detail.DetailView):
    model=Movies

class MoviesDeleteView(LoginRequiredMixin, DeleteView):
    model = Movies

    success_url = reverse_lazy('movies')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not obj.user == self.request.user:
            # Jeśli użytkownik nie jest właścicielem filmu, zwróć błąd
            return render(request, 'registration/unauthorized_access.html')
        return super().dispatch(request, *args, **kwargs)

class MoviesCreateView(LoginRequiredMixin, generic.edit.CreateView):
    model=Movies
    fields=['title','year', 'country']
    template_name = 'genericviewsDemo/movies_form.html'

    def get_success_url(self):
        return reverse_lazy('movies')
    def form_valid(self,form):
        form.instance.user=self.request.user
        return super().form_valid(form)

class MoviesEditView(LoginRequiredMixin, generic.edit.UpdateView):
    model=Movies
    fields=['title','year', 'country']
    template_name = 'genericviewsDemo/movies_form.html'

    def get_success_url(self):
        return reverse_lazy('movies')
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not obj.user == self.request.user:
            # Jeśli użytkownik nie jest właścicielem filmu, zwróć błąd
            return render(request, 'registration/unauthorized_access.html')
        return super().dispatch(request, *args, **kwargs)


    #def post(self, request, pk):
    #    my_object = get_object_or_404(Movies, pk=pk, user=request.user)
    #    form = MovieForm(request.POST, instance=my_object)
    #    if form.is_valid():
    #        form.save()
    #        return redirect('movies')  # Przekieruj użytkownika z powrotem do listy obiektów
    #    else:
    #        return redirect('edit', pk=pk)
    #        #return render(request, 'edit_object.html', {'form': form})
    #def get(self, request, pk):
    #    my_object = get_object_or_404(Movies, pk=pk, user=request.user)
    #    form = MovieForm(instance=my_object)
    #    return render(request, 'genericviewsDemo/edit_object.html', {'form': form})




