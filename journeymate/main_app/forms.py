from django.forms import ModelForm
from .models import Itinerary, Blog


class ItineraryForm(ModelForm):
    class Meta:
        model = Itinerary
        fields = ["date", "time", "activities"]

class BlogForm(ModelForm):
    class Meta:
        model = Blog
        fields = ["destination_name", "trip_post"]
