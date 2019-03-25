from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('',TemplateView.as_view(template_name='Controller/home.html'), name='home'),
    path('config/',TemplateView.as_view(template_name="Controller/config.html"),name='asds'),
    path('configurate/', views.send_shit, name ='config'),
   
]