from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import F
from django.http import JsonResponse
from geopy.distance import geodesic
from itertools import permutations
import networkx as nx
import django_filters
from .models import *
from .forms import *



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

    # trips = trips.order_by('-rating')

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



@login_required(login_url='login')
def data_filter(request):
    types = Trip.objects.values('trip_type').distinct()

    trip_filter = TripFilters(request.GET, queryset=Trip.objects.all())

    if 'trip_type' not in request.GET or request.GET['trip_type'] == '':
        trips = Trip.objects.all()
    else:
        trips = trip_filter.qs

    context = {
        'types': types,
        'filter': trip_filter,
    }
    return render(request, 'TourBUddy/data_filter.html', context)


@login_required(login_url='login')
def data_map(req):
    places = list(Trip.objects.values('latitude','longitude'))

    context = {'places':places}
    return render(req, 'TourBuddy/result.html', context)


@login_required(login_url='login')
def details(req, trip_id):
    data = get_object_or_404(Trip, pk=trip_id)
    
    place = Trip.objects.values('latitude', 'longitude').filter(pk=trip_id).first()

    context = {'place': place, 'data': data}
    return render(req, 'TourBUddy/details.html', context)


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



@login_required(login_url='login')
def search_data(req):
    query = req.GET.get('query')
    results = []
    if query:
        results = Trip.objects.filter(Q(trip_type__icontains=query) | Q(name__icontains=query))
    return render(req,'TourBUddy/home.html',{'query':query,'results':results})


def distances(req):
    latitude = float(req.GET.get('latitude'))
    longitude = float(req.GET.get('longitude'))
    user_location = (latitude, longitude)
    all_distances = {}

    for place in Trip.objects.all():
        place_location = (place.latitude, place.longitude)
        distance = geodesic(user_location, place_location).km
        all_distances[distance] = place_location

    min_distance = min(all_distances.keys())
    place_coords = all_distances[min_distance]

    return JsonResponse({
        'coordinates': place_coords,
        'distance': min_distance
    })


def make_tsp_graph(cities):
    """
    Create a complete graph representing all possible paths between cities.
    """
    G = nx.Graph()

    for trip in cities:
        G.add_node(trip)

    for trip1, trip2 in permutations(cities, 2):
        distance = trip1.distance_to(trip2) 
        G.add_edge(trip1, trip2, weight=distance)

    return G


def tsp_christofides(graph):
    """
    Find an approximate solution to the Traveling Salesman Problem using the Christofides Algorithm.
    """
    cycle = nx.approximation.traveling_salesman.christofides(graph, weight="weight")
    edge_list = list(nx.utils.pairwise(cycle))

    tsp_route = edge_list + [edge_list[0]]

    return tsp_route


def show_tsp_graph(request):
    all_trips = Trip.objects.all()

    cities = [trip for trip in all_trips]

    tsp_graph = make_tsp_graph(cities)

    cycle = nx.approximation.traveling_salesman.christofides(tsp_graph, weight="weight")
    
    tsp_route_coordinates = [(trip.latitude, trip.longitude) for trip in cycle]

    return JsonResponse({'tsp_route': tsp_route_coordinates})


def create_TouristNode(req, id):
    tour = Trip.objects.get(pk=id)
    
    ex_tour = TouristNode.objects.filter(user=req.user, trip=tour).first()

    if not ex_tour:
        TouristNode.objects.create(user=req.user, trip=tour)

    return redirect('/')

def Delete_item(req,id):
    data = TouristNode.objects.get(pk=id)
    data.delete()
    return redirect('read_basket')
