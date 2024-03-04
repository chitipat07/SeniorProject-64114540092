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
import folium
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


# def distances(req):
#     latitude = float(req.GET.get('latitude'))
#     longitude = float(req.GET.get('longitude'))
#     user_location = (latitude, longitude)
#     all_distances = {}

#     for place in Trip.objects.all():
#         place_location = (place.latitude, place.longitude)
#         distance = geodesic(user_location, place_location).km
#         all_distances[distance] = place_location

#     min_distance = min(all_distances.keys())
#     place_coords = all_distances[min_distance]

#     return JsonResponse({
#         'coordinates': place_coords,
#         'distance': min_distance
#     })
###########################################################################################################################
# ใช้จริง
# def distrip(req):
#     user_latitude = float(Order_Trip.objects.filter(user=req.user).values('user_latitude')[0]['user_latitude'])
#     user_longitude = float(Order_Trip.objects.filter(user=req.user).values('user_longitude')[0]['user_longitude'])
#     user_location = (user_latitude,user_longitude)
#     all_distances = {}
    
#     for place in TouristNode.objects.filter(user=req.user):
#         place_location = (float(place.trip.latitude), float(place.trip.longitude))
#         distance = geodesic(user_location, place_location).km
#         all_distances[place] = distance
    
#     return all_distances


def distrip(req):
    user_order_trip = Order_Trip.objects.filter(user=req.user).first()
    if user_order_trip:
        user_latitude = float(user_order_trip.user_latitude)
        user_longitude = float(user_order_trip.user_longitude)
        user_location = (user_latitude,user_longitude)
        all_distances = {}
        
        for place in TouristNode.objects.filter(user=req.user):
            place_location = (float(place.trip.latitude), float(place.trip.longitude))
            distance = geodesic(user_location, place_location).km
            all_distances[place] = distance
        
        return all_distances
    else:
        return {}


def make_tsp_graph(user_location, cities):
    """
    Create a complete graph representing all possible paths between user location and cities.
    """
    G = nx.Graph()

    G.add_node("User", pos=user_location)

    for place in cities:
        G.add_node(place, pos=(cities[place].latitude, cities[place].longitude))

    for place in cities:
        distance = geodesic(user_location, (cities[place].latitude, cities[place].longitude)).km
        G.add_edge("User", place, weight=distance)

    for place1, place2 in permutations(cities, 2):
        distance = geodesic((cities[place1].latitude, cities[place1].longitude),
                            (cities[place2].latitude, cities[place2].longitude)).km
        G.add_edge(place1, place2, weight=distance)

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
    user_order_trip = Order_Trip.objects.filter(user=request.user).first()
    if user_order_trip:
        user_latitude = float(user_order_trip.user_latitude)
        user_longitude = float(user_order_trip.user_longitude)
        user_location = (user_latitude, user_longitude)

        all_trips = TouristNode.objects.filter(user=request.user)

        cities = {}
        for trip in all_trips:
            cities[trip.trip.name] = trip.trip

        tsp_graph = make_tsp_graph(user_location, cities)

        cycle = nx.approximation.traveling_salesman.christofides(tsp_graph, weight="weight")
        
        tsp_route_coordinates = [(tsp_graph.nodes[node]["pos"]) for node in cycle]

        return JsonResponse({'tsp_route': tsp_route_coordinates})
    else:
        return JsonResponse({'error': 'No user location found'})

###########################################################################################################################

# def make_tsp_graph(cities):
#     """
#     Create a complete graph representing all possible paths between cities.
#     """
#     G = nx.Graph()

#     for trip in cities:
#         G.add_node(trip)

#     for trip1, trip2 in permutations(cities, 2):
#         distance = trip1.distance_to(trip2) 
#         G.add_edge(trip1, trip2, weight=distance)

#     return G


# def tsp_christofides(graph):
#     """
#     Find an approximate solution to the Traveling Salesman Problem using the Christofides Algorithm.
#     """
#     cycle = nx.approximation.traveling_salesman.christofides(graph, weight="weight")
#     edge_list = list(nx.utils.pairwise(cycle))

#     tsp_route = edge_list + [edge_list[0]]

#     return tsp_route


# def show_tsp_graph(request):
#     all_trips = Trip.objects.all()

#     cities = [trip for trip in all_trips]

#     tsp_graph = make_tsp_graph(cities)

#     cycle = nx.approximation.traveling_salesman.christofides(tsp_graph, weight="weight")
    
#     tsp_route_coordinates = [(trip.latitude, trip.longitude) for trip in cycle]

#     return JsonResponse({'tsp_route': tsp_route_coordinates})
###########################################################################################################################

def create_TouristNode(req, id):
    tour = Trip.objects.get(pk=id)
    
    ex_tour = TouristNode.objects.filter(user=req.user, trip=tour).first()

    if not ex_tour:
        TouristNode.objects.create(user=req.user, trip=tour)

    return redirect('/')


def Delete_item(req,id):
    data = TouristNode.objects.get(pk=id)
    data.delete()
    return redirect('read_TouristNode')


def read_TouristNode(request):
    data = TouristNode.objects.filter(user=request.user)
    return render(request,'TourBUddy/read_tour.html', {'data': data})


def Notti(request):
    n = TouristNode.objects.filter(user=request.user).count()
    return JsonResponse({'n': n})

def current_location(req):
    return render(req,'TourBUddy/current_location.html')


def confirm(req):
    if req.method == 'POST':
        latitude = req.POST.get('user_latitude')
        longitude = req.POST.get('user_longitude')
        
        basket = TouristNode.objects.filter(user=req.user).first()
        
        order = Order_Trip.objects.create(
            user=req.user,
            item_trip=basket,
            user_latitude=latitude,
            user_longitude=longitude
        )

        
        return redirect('data_map')


@login_required(login_url='login')
def data_map(req):
    places = list(TouristNode.objects.filter(user=req.user).select_related('trip').values('trip__latitude', 'trip__longitude','trip__name','trip__image'))

    user_locations = list(Order_Trip.objects.filter(user=req.user).values('user_latitude', 'user_longitude'))

    data = TouristNode.objects.filter(user=req.user)

    context = {'places':places,'user_locations': user_locations,'data':data}
    return render(req, 'TourBuddy/result.html', context)



# def data_popup(req):
#     data = TouristNode.objects.filter(user=req.user)

#     m = folium.Map(location=[15.2302166, 104.8572949],zoom_start=9)

#     for place in data:
#         coor = (place.trip__latitude,place.trip__longitude)
#         folium.Marker(coor,popup=place.trip__name).add_to(m)

#     context = {'map':m._repr_html_()}
#     return render(req,'TourBuddy/show_map.html',context)


    

# def distance_to(self, other_trip):
#         """
#         Calculate the distance between two trips using their latitude and longitude.
#         """
#         lat1 = radians(self.latitude)
#         lon1 = radians(self.longitude)
#         lat2 = radians(other_trip.latitude)
#         lon2 = radians(other_trip.longitude)

#         R = 6371.0

#         dlat = lat2 - lat1
#         dlon = lon2 - lon1

#         a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
#         c = 2 * atan2(sqrt(a), sqrt(1 - a))
#         distance = R * c

#         return distance
