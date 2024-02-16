from . import views
from django.urls import path


urlpatterns = [
    path('movies/', views.MovieListView.as_view(), name='movies'),
    path('create/', views.MoviesCreateView.as_view(), name='create'),
    path('movie/<int:pk>/', views.MovieDetailView.as_view(), name='movie'),
    path('delete/<int:pk>/', views.MoviesDeleteView.as_view(), name='delete'),
    path('edit/<int:pk>/', views.MoviesEditView.as_view(), name='edit'),

]