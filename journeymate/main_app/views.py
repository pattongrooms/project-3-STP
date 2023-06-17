from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Destination
from .forms import ItineraryForm

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
