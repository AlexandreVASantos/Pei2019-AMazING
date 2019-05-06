from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('getlogin/', views.getlogin, name='getLogin'),
    path('config/',views.send_grid,name='config'),
    path('config/change/', views.change_grid, name ='change'),
    path('logout/',views.log_out, name='logout'),
    path('login/',views.log_in, name='login'),
    path('nodeup/',views.node_up, name='node_up'),
    path('config/refresh/',views.grid_update, name='update'),
    path('notifications/', views.notifications, name= 'notifications'),
    path('notifications/date/', views.get_notifications_with_date, name= 'get_alert_date'),
    path('sensors/', views.sensors, name= 'sensors'),
    path('password/', views.password, name = 'password'),
    path('password/change/', views.change_pass, name = 'change_pass'),
    path('manual/', views.manual, name='manual'),
    
   
]