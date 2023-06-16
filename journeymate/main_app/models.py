from django.db import models

# Create your models here.

TRANSPORTS = (
  ('A', 'Airplane'),
  ('T', 'Train'),
  ('D', 'Drive'),
  ('B', 'Bus'),
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