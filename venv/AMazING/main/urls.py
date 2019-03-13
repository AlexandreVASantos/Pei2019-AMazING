from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views


urlpatterns = [
    path('',views.home, name='main'),
    path('about/',views.about, name='about')
]

urlpatterns += staticfiles_urlpatterns()