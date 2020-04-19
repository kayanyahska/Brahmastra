from django.db import models
from django.utils import timezone

class Volunteer(models.Model):
    phone_number = models.IntegerField()
    reported_date = models.DateTimeField(default = timezone.now)
    lat = models.DecimalField(max_digits=10,decimal_places=6)
    lon = models.DecimalField(max_digits=10,decimal_places=6)
    location = models.TextField(max_length=100)
    def updateLocation(self,lat,lon,location):
        self.lat=lat
        self.lon=lon
        self.location=location
    def __str__(self):
        return str(self.id)
        
class Victim(models.Model):
    phone_number = models.IntegerField()
    reported_date = models.DateTimeField(default = timezone.now)
    lat = models.DecimalField(max_digits=10,decimal_places=6)
    lon = models.DecimalField(max_digits=10,decimal_places=6)
    location=models.TextField(max_length=100)
    rescued = models.BooleanField(default=False)
    volunteer=models.ForeignKey(Volunteer, on_delete=models.CASCADE)

    def setRescued(self, val):
        self.rescued = val

    def updateLocation(self,lat,lon,location):
        self.lat=lat
        self.lon=lon
        self.location=location
        self.reported_date=timezone.now()

    def assign(self,volunteer):
        self.volunteer=volunteer

    def __str__(self):
        return str(self.id)