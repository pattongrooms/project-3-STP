import uuid
import boto3
import os
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Destination
from .forms import ItineraryForm, Media

# Create your views here.


def home(request):
    return render(request, "home.html")


def about(request):
    return render(request, "about.html")


def destinations_index(request):
    destinations = Destination.objects.all()
    return render(request, "destinations/index.html", {"destinations": destinations})


def destinations_detail(request, destination_id):
    destination = Destination.objects.get(id=destination_id)
    itinerary_form = ItineraryForm()
    return render(
        request,
        "destinations/detail.html",
        {"destination": destination, "itinerary_form": itinerary_form},
    )


def add_itinerary(request, destination_id):
    form = ItineraryForm(request.POST)
    if form.is_valid():
        new_itinerary = form.save(commit=False)
        new_itinerary.destination_id = destination_id
        new_itinerary.save()
    return redirect("detail", destination_id=destination_id)


def add_media(request, _id):
    media_file = request.FILES.get('media-file', None)
    if media_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + media_file.name[media_file.name.rfind('.'):]
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(media_file, bucket, key)
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            Media.objects.create(url=url, destination_id=destination_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('detail', destination_id=destination_id)


class DestinationCreate(CreateView):
    model = Destination
    fields = "__all__"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DestinationUpdate(UpdateView):
    model = Destination
    fields = "__all__"


class DestinationDelete(DeleteView):
    model = Destination
    success_url = "/destinations"
