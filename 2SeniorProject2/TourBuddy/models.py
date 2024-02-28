from django.db import models
from math import radians, sin, cos, sqrt, atan2
from django.contrib.auth.models import User


class Trip(models.Model):
    location = models.CharField(max_length=200)
    latitude = models.FloatField(null=True)  
    longitude = models.FloatField(null=True)
    name = models.CharField(max_length=100)
    rating = models.FloatField(null=True)
    review = models.TextField()
    trip_type = models.CharField(max_length=50)
    g_type = models.CharField(max_length=50,null=True)
    image = models.CharField(max_length=200)

    def __str__(self):
        return f' name {self.name} latitude {self.latitude} longitude {self.longitude}'
    

class TouristNode(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    trip = models.ForeignKey(Trip,on_delete=models.CASCADE,null=True,blank=True)
    


class Order_Trip(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    item_trip = models.ForeignKey(TouristNode,on_delete=models.CASCADE,null=True,blank=True)
    user_latitude = models.CharField(max_length=300,null=True)  
    user_longitude = models.CharField(max_length=300,null=True)

    def __str__(self):
        return f' user_latitude {self.user_latitude} user_longitude {self.user_longitude}'
