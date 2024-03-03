from . import views
from django.urls import path


urlpatterns = [
    path('', views.WpisyListView.as_view(), name='main'),
    path('search/<path:query>', views.SearchView.as_view(), name='search'),
    path('search/', views.WpisyListView.as_view(), name='search1'),
    path('comment/<int:pk>/', views.KomentarzCreateView.as_view(), name='dodaj_komentarz'),
    path('profile/edit', views.EditBio.as_view(), name='editbio'),
     path('post/delete/<int:pk>', views.PostDeleteView.as_view(), name='deletepost'),
    path('comment/delete/<int:pk>', views.CommentDeleteView.as_view(), name='deletecomment'),
    path('profile/<username>/', views.ProfilePage.as_view(), name='profile'),
    path('post/vote/<int:pk>/', views.upvote, name='vote'),
    path('post/downvote/<int:pk>/', views.downvote, name='downvote'),
]