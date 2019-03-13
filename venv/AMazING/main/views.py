from django.shortcuts import render
from django.http import HttpResponse

def home(request):
	return render(request,'main/login.html')

def about(request):
	return HttpResponse('<h1> about </h1>')