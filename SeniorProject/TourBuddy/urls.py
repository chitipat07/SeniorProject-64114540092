from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name='home'),
    path('register/',register,name='register'),
    path('login/',logins,name='login'),
    path('logout/',logout_view,name='logout'),
    path('search/',search_data,name='search'),
    path('details/<int:trip_id>/',details, name='details'),
    path('data_map/',data_map, name='data_map'),

    
]