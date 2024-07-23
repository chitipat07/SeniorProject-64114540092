from django.urls import path
from .views import *

urlpatterns = [
    path('admin_page/',admin_page,name='admin_page'),
    path('list_users/',list_users,name='list_users'),
    path('create_trip/',create_trip,name='create_trip'),
    path('update_trip/<int:pk>/', update_trip, name='update_trip'),
    path('delete/<int:id>/',delete_trip,name='delete'),
    path('delete_user/<int:pk>/', delete_user, name='delete_user'),
]