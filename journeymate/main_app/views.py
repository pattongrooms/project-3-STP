from django.shortcuts import render
from .models import Destination

# Create your views here.

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def destinations_index(request):
  destinations = Destination.objects.all()
  return render(request, 'destinations/index.html', {
    'destinations': destinations
  })


