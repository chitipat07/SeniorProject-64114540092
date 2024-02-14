from django.contrib import admin
from .models import *
# Register your models here.
class TripAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'latitude', 'longitude', 'rating', 'trip_type', 'g_type')

class TouristNodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'trip')

class OrderTripAdmin(admin.ModelAdmin):
    list_display = ('user', 'item_trip', 'user_latitude', 'user_longitude')

admin.site.register(Trip)
admin.site.register(TouristNode)
admin.site.register(Order_Trip)