import uuid
import boto3
import os
import requests
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Destination, Media, Blog
from .forms import ItineraryForm

# Create your views here.


def home(request):
    return render(request, "home.html")


def about(request):
    return render(request, "about.html")


@login_required
def destinations_index(request):
    destinations = Destination.objects.filter(user=request.user)
    return render(request, "destinations/index.html", {"destinations": destinations})


@login_required
def destinations_detail(request, destination_id):
    destination = Destination.objects.get(id=destination_id)
    itinerary_form = ItineraryForm()
    return render(
        request,
        "destinations/detail.html",
        {"destination": destination, "itinerary_form": itinerary_form},
    )

@login_required
def weather(request):
  key = os.environ['WEATHER_ACCESS_KEY']
  url = f'http://api.openweathermap.org/data/2.5/weather?q=Boston&units=imperial&APPID={key}'
  city = 'Boston'
  r = requests.get(url.format(city)).json()

  destination_weather = {
    'city': city,
    'temperature': r['main']['temp'],
    'description': r['weather'][0]['description'],
    'icon': r['weather'][0]['icon'],
  }

  context = {'destination_weather': destination_weather}

  return render(request, 'destinations/weather/weather.html', context)


@login_required
def add_itinerary(request, destination_id):
    form = ItineraryForm(request.POST)
    if form.is_valid():
        new_itinerary = form.save(commit=False)
        new_itinerary.destination_id = destination_id
        new_itinerary.save()
    return redirect("detail", destination_id=destination_id)


@login_required
def add_media(request, destination_id):
    media_file = request.FILES.get('media-file', None)
    if media_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + \
            media_file.name[media_file.name.rfind('.'):]
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(media_file, bucket, key)
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            Media.objects.create(url=url, destination_id=destination_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('detail', destination_id=destination_id)


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


class DestinationCreate(LoginRequiredMixin, CreateView):
    model = Destination
    fields = ['start_date', 'end_date', 'country',
              'state', 'city', 'transportation', 'accomodations']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DestinationUpdate(LoginRequiredMixin, UpdateView):
    model = Destination
    fields = "__all__"


class DestinationDelete(LoginRequiredMixin, DeleteView):
    model = Destination
    success_url = "/destinations"


class BlogPostCreate(LoginRequiredMixin, CreateView):
  model = Blog
  fields = ['destination_name', 'trip_post']

  def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

