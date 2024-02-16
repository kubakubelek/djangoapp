from django.urls import path

from . import views

urlpatterns = [
    path('game', views.game),
    path("danger", views.danger),
    path('main/<slug:guess>', views.MainView.as_view()),
    path('main', views.BounceView.as_view()),
    path('bounce', views.bounce),

]