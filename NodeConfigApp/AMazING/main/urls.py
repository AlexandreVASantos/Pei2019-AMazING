from django.urls import path
from . import views


urlpatterns = [
    path('',views.home, name=''),
    path('getApIp/',views.postGetApIP,name='getApIp'),
    path('LocalW/',views.postLocalWireless,name='LocalW'),
    path('StopAccessP/',views.postStopAccessPoint,name='StopAccessP'),
    path('nodeCompare/',views.compare_owner,name='nodeCompare'),
    path('nodeChange/',views.postTurnOnNode,name='nodeChange'),
    path('logout/',views.Logout,name='logout'),
    path('auth/',views.auth, name='auth'),
    path('about/',views.about, name='about'),
    path('menu/',views.menu, name='menu'),
    path('AccessP/',views.AccessP, name='AccessP'),
    path('postAccessP/',views.postAccessP, name='postAccessP'),
    path('NodeMenu/',views.NodeMenu, name='NodeMenu'),
    path('modBitrate/',views.modBitrate, name='modBitrate'),
    path('postModBitrate/',views.postModBitrate, name='postModBitrate'),
    path('postIPChange/',views.postIPChange, name='postIPChange'),
    path('postConnection/',views.postConnection, name='postConnection'),
    path('postDisconnect/',views.postDisconnect, name='postDisconnect'),
    path('postStationPeer/',views.postStationPeer, name='postStationPeer'),    
    path('connection/',views.connection, name='connection'),
    path('postScanning/',views.postScanning, name='postScanning'),
    path('postLinkStatus/',views.postLinkStatus, name='postLinkStatus'),
    path('postStationStats/',views.postStationStats, name='postStationStats'),
    path('setTxPower/',views.setTxPower, name='setTxPower'),
    path('postTxPower/',views.postTxPower, name='postTxPower'),
    path('help/',views.help, name='help'),
    path('stationPeer/',views.stationPeer, name='stationPeer'),
    path('addrChange/',views.addrChange, name='addrChange')
]

views.consumer(repeat_until=None)