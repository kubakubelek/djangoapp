from django.urls import path

from . import views

urlpatterns = [
    path('game/<slug:guess>', views.GameView.as_view()),
]