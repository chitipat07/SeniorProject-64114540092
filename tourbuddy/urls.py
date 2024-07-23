from django.urls import path
from django.contrib.auth import views
from .views import *

urlpatterns = [
    path('',indexcard1,name='indexcard1'),
    path('showdatamore/', showdatamore, name='showdatamore'),
    path('signup/',signup,name='signup'),
    path('login_view/',views.LoginView.as_view(template_name='tourbuddy/login.html'),name='login_view'),
    path('logout/',views.LogoutView.as_view(),name='logout'),
    path('details/<int:trip_id>/',details, name='details'),
    path('search_data/',search_data, name='search_data'),
    path('data_filter/',data_filter, name='data_filter'),
    path('home_get_plan/',home_get_plan, name='home_get_plan'),
    path('Notti/', Notti, name='Notti'),
    path('create_TouristNode/<int:id>/', create_TouristNode, name='create_TouristNode'),
    path('data_filter2/',data_filter2, name='data_filter2'),
    path('search_data2/',search_data2, name='search_data2'),
    path('read_TouristNode/',read_TouristNode, name='read_TouristNode'),
    path('Notti0/',Notti0, name='Notti0'),
    path("current_location/",current_location,name='current_location'),
    path("confirm/",confirm,name='confirm'),
    path('data_map/',data_map, name='data_map'),
    path('show_tsp_graph/', show_tsp_graph, name='show_tsp_graph'),
    path("delete_item/<int:id>/",Delete_item,name='delete_item'),
    path("my_view/",my_view,name='my_view'),
    path("update_user_location/", update_user_location, name='update_user_location'),
    path("update_current_location/",update_current_location,name='update_current_location'),
    path("distrip2/",distrip2,name='distrip2'),
    path("get_all_routes_and_places/",get_all_routes_and_places,name='get_all_routes_and_places'),
    path("data_map2/",data_map2,name='data_map2'),
    path("test_trip/",test_trip,name='test_trip')

    




]