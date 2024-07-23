from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import django_filters
from .models import *

class SignUpforms(UserCreationForm):
   first_name = forms.CharField(max_length=50,required=True)
   last_name = forms.CharField(max_length=50,required=True)
   email = forms.EmailField(max_length=255,required=True)

   class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']

class TripFilters(django_filters.FilterSet):
    trip_type = django_filters.CharFilter(field_name='trip_type', lookup_expr='iexact')

    class Meta:
        model = Trip
        fields = ['trip_type']