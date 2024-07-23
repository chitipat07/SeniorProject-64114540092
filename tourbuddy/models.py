from django.db import models
from django.contrib.auth.models import User


class Trip(models.Model):
    location = models.CharField(max_length=600)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    name = models.CharField(max_length=500)
    rating = models.FloatField(null=True, blank=True)
    review = models.CharField(max_length=500,null=True, blank=True)
    trip_type = models.CharField(max_length=500)
    g_type = models.CharField(max_length=500, null=True, blank=True)
    image = models.CharField(max_length=600)

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