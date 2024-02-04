from django.db import models


class Trip(models.Model):
    location = models.CharField(max_length=200)
    latitude = models.FloatField(null=True)  
    longitude = models.FloatField(null=True)
    name = models.CharField(max_length=100)
    rating = models.FloatField(null=True)
    review = models.TextField()
    trip_type = models.CharField(max_length=50)
    image = models.CharField(max_length=200)

    def __str__(self):
        return f' name {self.name} latitude {self.latitude} longitude {self.longitude}'


# class TouristNode(models.Model):
#     trip = models.ForeignKey(Trip,on_delete=models.CASCADE,null=True,blank=True)
#     node = models.IntegerField(null=True)
#     distance = models.FloatField(null=True)

#     def __str__(self):
#         return f'Trip: {self.trip}, Node: {self.node}'