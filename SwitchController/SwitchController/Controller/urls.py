from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('',TemplateView.as_view(template_name='Controller/home.html'), name='home'),
    path('config/',views.send_grid,name='config'),
    path('configurate/', views.send_shit, name ='configurate'),
   
]