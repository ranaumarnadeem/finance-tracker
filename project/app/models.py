from django.db import models # type: ignore

class menuitem(models.Model):
    name = models.CharField(max_length=256)
    price = models.IntegerField()

class Reservation(models.Model):
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    guest= models.IntegerField()
    reservation_time = models.DateField(auto_now=True)
    comments = models.CharField(max_length=1000)