from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.db.models import Q
import folium
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import F
import django_filters
from .models import *
from .forms import *
# Create your views here.


class TripFilters(django_filters.FilterSet):
    trip_type = django_filters.CharFilter(field_name='trip_type', lookup_expr='iexact')

    class Meta:
        model = Trip
        fields = ['trip_type']


def home(request):
    data = Trip.objects.all()
    types = Trip.objects.values('trip_type').distinct() 

    trip_filter = TripFilters(request.GET, queryset=Trip.objects.all())

    if 'trip_type' not in request.GET or request.GET['trip_type'] == '':
        trips = Trip.objects.all()
    else:
        
        trips = trip_filter.qs

    paginator = Paginator(trips, 28)
    page = request.GET.get('page')

    try:
        data_page = paginator.page(page)
    except PageNotAnInteger:
        data_page = paginator.page(1)
    except EmptyPage:
        data_page = paginator.page(paginator.num_pages)

    context = {
        'trips': data_page,
        'filter': trip_filter,
        'types': types,
    }

    return render(request, 'TourBUddy/home.html', {'context':context, 'types': types,'data_page': data_page,'data':data})


def data_map(req):
    places = Trip.objects.all()

    m = folium.Map(location=[15.2302166, 104.8572949], zoom_start=10)

    for place in places:
        c = [place.latitude, place.longitude]
        folium.Marker(location=c,popup=place.name).add_to(m)

    context = {'map': m._repr_html_()}
    return render(req, 'TourBuddy/result.html', context)



def details(req, trip_id):
    data = get_object_or_404(Trip, pk=trip_id)
    return render(req, 'TourBUddy/details.html', {'data': data})

def register(req):
    form = Userforms()
    if req.method == 'POST':
        form = Userforms(req.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = Userforms()

    return render(req,'TourBuddy/register.html',{'form':form})

def logins(req):
        form = Loginforms()
        if req.method == 'POST':
            form = Loginforms(req.POST)
            if form.is_valid:
                username = req.POST.get('username')
                password = req.POST.get('password')
                user = authenticate(username=username,password=password)
                if user:
                    login(req,user)
                    return redirect('home')
        return render(req, 'TourBuddy/login.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect('home')

def search_data(req):
    query = req.GET.get('query')
    results = []
    if query:
        results = Trip.objects.filter(Q(trip_type__icontains=query) | Q(name__icontains=query))
    return render(req,'TourBUddy/home.html',{'query':query,'results':results})

# def search_view(request):
#     all_people = User.objects.all()
#     context = {'count': all_people.count()}
#     return render(request, 'search.html', context)


# def search_results_view(request):
#     query = request.GET.get('search', '')
#     print(f'{query = }')

#     all_people = User.objects.all()
#     if query:
#         people = all_people.filter(username__icontains=query)
#     else:
#         people = []

#     context = {'people': people, 'count': all_people.count()}
#     return render(request, 'search_results.html', context)


# def filtered_type(req):
#     types = Trip.objects.all()
#     filtered_trips = Trip.objects.filter(trip_type=types)
#     return render(req,'TourBUddy/filter.html',{'types':types,'filtered_trips':filtered_trips})



# form = Loginforms()

#     if request.method == 'POST':
#         form = Loginforms(request.POST)
#         if form.is_valid:
#             username = request.POST.get('username')
#             password = request.POST.get('password')
#             user = authenticate(username=username,password=password)
#             if user:
#                 login(request,user)
#                 return redirect('/')