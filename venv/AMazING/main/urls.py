from django.urls import path
from . import views


urlpatterns = [
    path('',views.home, name='login'),
    path('about/',views.about, name='about'),
    path('menu/',views.menu, name='menu'),
    path('NodeMenu/',views.NodeMenu, name='NodeMenu'),
    path('connect/',views.post, name='connect'),
    path('connection/',views.connection, name='connection'),
    path('main/',views.main, name='main'),
    path('help/',views.help, name='help'),
    path('get/',views.get, name='get'),
    path('stationPeer/',views.stationPeer, name='stationPeer'),
    path('addrChange/',views.addrChange, name='addrChange')
]
