from django.db import models
from django.urls import reverse

# Create your models here.

TRANSPORTS = (
  ('A', 'Airplane'),
  ('T', 'Train'),
  ('D', 'Drive'),
  ('B', 'Bus'),
)


ACCOMODATIONS = (
  ('H', 'Hotel'),
  ('A', 'AirBnB'),
  ('F', 'Friend'),
)

class Destination(models.Model):
  start_date = models.DateField('Start Date')
  end_date = models.DateField('End Date')
  country = models.CharField(max_length=100)
  state = models.CharField(max_length=100)
  city = models.CharField(max_length=100)
  transportation = models.CharField(
    max_length=1,
    choices=TRANSPORTS,
    default=TRANSPORTS[0][0],
  )
  accomodations = models.CharField(
    max_length=1,
    choices=ACCOMODATIONS,
    default=ACCOMODATIONS[0][0],
  )
  
  
  def __str__(self): 
    return f'{self.country} ({self.id})'

  def get_absolute_url(self):
    return reverse('detail', kwargs={'destination_id': self.id})