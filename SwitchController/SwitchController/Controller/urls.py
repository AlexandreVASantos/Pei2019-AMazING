from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('getlogin/', views.getlogin, name='getLogin'),
    path('config/',views.send_grid,name='config'),
    path('configurate/', views.send_shit, name ='configurate'),
    path('logout/',views.log_out, name='logout'),
    path('login/',views.log_in, name='login'),
   
]