from . import views
from django.urls import path

urlpatterns = [
    path('', views.MainView.as_view(), name='list'),
    path('user/<int:pk>', views.MainView.as_view(), name='detail'),
    path('login', views.LoginView.as_view(), name='login'),
    path('register', views.RegisterView.as_view(), name='register'),
]