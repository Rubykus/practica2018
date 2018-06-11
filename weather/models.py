from django.db import models


class Weather(models.Model):
    city_name = models.CharField(max_length=200)
    temp = models.FloatField()
    pressure = models.FloatField()
    wind_speed = models.FloatField()
    date = models.DateTimeField()

    class Meta:
        unique_together = ('city_name', 'date')
