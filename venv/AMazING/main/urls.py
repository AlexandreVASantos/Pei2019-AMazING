from django.urls import path
from . import views


urlpatterns = [
    path('',views.home, name=''),
    path('about/',views.about, name='about'),
    path('menu/',views.menu, name='menu'),
    path('NodeMenu/',views.NodeMenu, name='NodeMenu'),
    path('postIPChange/',views.postIPChange, name='postIPChange'),
    path('postConnection/',views.postConnection, name='postConnection'),
    path('postEventListening/',views.postEventListening, name='postEventListening'),
    path('postStationPeer/',views.postStationPeer, name='postStationPeer'),    
    path('connection/',views.connection, name='connection'),
    path('postScanning/',views.postScanning, name='postScanning'),
    path('postLinkStatus/',views.postLinkStatus, name='postLinkStatus'),
    path('postStationStats/',views.postStationStats, name='postStationStats'),
    path('postStationPeer/',views.postStationStats, name='postStationStats'),
    path('get/',views.get, name='get'),
    path('setTxPower/',views.setTxPower, name='setTxPower'),
    path('postTxPower/',views.postTxPower, name='postTxPower'),
    path('help/',views.help, name='help'),
    path('get/',views.get, name='get'),
    path('stationPeer/',views.stationPeer, name='stationPeer'),
    path('addrChange/',views.addrChange, name='addrChange')
]

views.consumer()