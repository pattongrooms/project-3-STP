from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

# Create your models here.

TRANSPORTS = (
    ("A", "Airplane"),
    ("T", "Train"),
    ("D", "Drive"),
    ("B", "Bus"),
)


ACCOMODATIONS = (
    ("H", "Hotel"),
    ("A", "AirBnB"),
    ("F", "Friend"),
)


class Destination(models.Model):
    start_date = models.DateField("Start Date")
    end_date = models.DateField("End Date")
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    transportation = models.CharField(max_length=100)
    accomodations = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.country} ({self.id})"

    def get_absolute_url(self):
        return reverse("detail", kwargs={"destination_id": self.id})

    def activity_for_today(self):
        return self.itinerary_set.count() >= 1


class Itinerary(models.Model):
    date = models.DateField("Itinerary Date")
    time = models.CharField(max_length=8)
    activities = models.TextField(max_length=250)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_activity_display()} on {self.date} and {self.activities}"

    def get_absolute_url(self):
        return reverse("detail", kwargs={"destination_id": self.destination.id})

    class Meta:
        ordering = ["-date", "time"]


class Media(models.Model):
    url = models.CharField(max_length=200)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)

    def __str__(self):
        return f"Media for destination_id: {self.destination_id} @{self.url}"


class Blog(models.Model):
    destination_name = models.CharField("Journey", max_length=100)
    trip_post = models.TextField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Blog post for blog_id: {self.id}"

    def get_absolute_url(self):
        return reverse("home")
