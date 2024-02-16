from django.urls import path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    #path("", views.response, name="response"),
    path('', views.main, name='main'),
    path('shuffle_divs/', views.shuffle_divs, name='shuffle_divs'),
    #path('', TemplateView.as_view(template_name='main/main.html'))
]