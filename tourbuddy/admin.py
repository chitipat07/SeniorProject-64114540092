from django.contrib import admin
from .models import *
# Register your models here.
class Order_TripAdmin(admin.ModelAdmin):
    list_display = ('user', 'item_trip', 'user_latitude', 'user_longitude')

class TouristNodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'trip')
    
class TripAdmin(admin.ModelAdmin):
    list_display = ('location', 'latitude', 'longitude', 'name', 'rating', 'review', 'trip_type', 'g_type', 'image')

admin.site.register(Trip, TripAdmin)
admin.site.register(TouristNode,TouristNodeAdmin)
admin.site.register(Order_Trip, Order_TripAdmin)
