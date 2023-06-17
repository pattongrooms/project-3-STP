from django.contrib import admin
from .models import Destination, Itinerary, Media

# Register your models here.
admin.site.register(Destination)
admin.site.register(Itinerary)
admin.site.register(Media)
