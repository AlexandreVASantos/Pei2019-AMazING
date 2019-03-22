from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views


urlpatterns = [
    path('',views.login, name='login'),
    path('login/',views.login, name='login'),
    path('about/',views.about, name='about'),
    path('main/',views.main, name='main')
]

urlpatterns += staticfiles_urlpatterns()