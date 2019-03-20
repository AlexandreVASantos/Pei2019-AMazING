from django.shortcuts import render


# Create your views here.
def home(request):
	return render(request,'Controller/home.html')

def config(request):
	return render(request,'Controller/config.html')