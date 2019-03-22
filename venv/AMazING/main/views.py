from django.shortcuts import render
from django.http import HttpResponse

def login(request):
	return render(request,'main/login.html')

def about(request):
	return render(request, 'main/about.html')

def main(request):
	return render(request, 'main/main.html')