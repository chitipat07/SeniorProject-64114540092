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
    path('data_filter/',data_filter, name='data_filter'),
    # path('get-nearest-place/',distances, name='distances'),
    path('show_tsp_graph/', show_tsp_graph, name='show_tsp_graph'),
    path('create_TouristNode/<int:id>/', create_TouristNode, name='create_TouristNode'),
    path("delete_item/<int:id>/",Delete_item,name='delete_item'),
    path("read_TouristNode/",read_TouristNode,name='read_TouristNode'),
    path("current_location/",current_location,name='current_location'),
    path('n/', Notti, name='n'),
    path("confirm/",confirm,name='confirm'),
    path("my_view/",my_view,name='my_view'),

    # path("data_popup/",data_popup,name='data_popup'),








]