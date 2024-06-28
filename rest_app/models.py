from django.db import models

class Touristplaces(models.Model):
    Name = models.CharField(max_length=200)
    Weather = models.CharField(max_length=200)
    Location_State = models.CharField(max_length=200)
    Location_District = models.CharField(max_length=200)
    Images = models.ImageField(upload_to='tour/')
    Description = models.CharField(max_length=300)
