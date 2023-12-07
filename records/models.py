from django.db import models
from .validators import *


# Create your models here.
class Record(models.Model):
    #  Here define an enum to map the possible weather conditions
    class Enumconditions(models.TextChoices):
        SUNNY = 1, "Sunny weather"
        CLOUDY = 2, "Cloudy weather"
        RAINY = 3, "Rainy weather"
        FLURRY = 4, "Flurry weather"  # Flurry = it's snowing bro

    humidity = models.IntegerField(validators=[validate_humidity])
    temperature = models.IntegerField(validators=[validate_temperature])
    wind = models.IntegerField(validators=[validate_wind])
    date = models.DateTimeField()  # TODO: Check if it works correctly
    created_at = models.DateTimeField(auto_now_add=True)
    condition = models.CharField(max_length=1, choices=Enumconditions.choices, default=Enumconditions.SUNNY)

    def __str__(self):
        return (f'Condition: {self.condition}, Humidity: {self.humidity}%, Temperature: {self.temperature} C°, '
                f'Wind: {self.wind} Km/h, Date: {self.date}')
