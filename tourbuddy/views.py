from django.shortcuts import render,redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .forms import SignUpforms,TripFilters
from django.shortcuts import get_object_or_404

from geopy.distance import geodesic
from itertools import permutations
import networkx as nx
import folium
from django.http import JsonResponse

def test_trip(req):
    data = Trip.objects.filter(trip_type="แลนด์มาร์กและอนุสรณ์สถาน/สวนและสวนสาธารณะ")
    c = Trip.objects.all().count()
    return render(req,'testtsp/test_trip.html',{'data':data,'c':c})



################ Showdata #################

def indexcard1(req):
    if req.user.is_authenticated and req.user.is_superuser:
        return redirect('admin_page') 
    data1 = Trip.objects.filter(trip_type="ท่องเที่ยวทางธรรมชาติ").order_by('-rating')[:3]
    count1 = Trip.objects.filter(trip_type="ท่องเที่ยวทางธรรมชาติ").count()

    data2 = Trip.objects.filter(trip_type="พิพิธภัณฑ์และการเรียนรู้").order_by('-rating')[:3]
    count2 = Trip.objects.filter(trip_type="พิพิธภัณฑ์และการเรียนรู้").count()

    data3 = Trip.objects.filter(trip_type="กิจกรรมและความบันเทิง").order_by('-rating')[:3]
    count3 = Trip.objects.filter(trip_type="กิจกรรมและความบันเทิง").count()

    data4 = Trip.objects.filter(trip_type="ประวัติศาสตร์ วัฒนธรรมและศาสนา").order_by('-rating')[:3]
    count4 = Trip.objects.filter(trip_type="ประวัติศาสตร์ วัฒนธรรมและศาสนา").count()

    data5 = Trip.objects.filter(trip_type="แลนด์มาร์กและอนุสรณ์สถาน/สวนและสวนสาธารณะ").order_by('-rating')[:3]
    count5 = Trip.objects.filter(trip_type="แลนด์มาร์กและอนุสรณ์สถาน/สวนและสวนสาธารณะ").count()

    types = Trip.objects.values('trip_type').distinct()

    trip_filter = TripFilters(req.GET, queryset=Trip.objects.all())

    if 'trip_type' not in req.GET or req.GET['trip_type'] == '':
        trips = Trip.objects.all()
    else:   
        trips = trip_filter.qs
    context = {
        'data1': data1,
        'data2': data2,
        'data3': data3,
        'data4': data4,
        'data5': data5,
        'count1': count1,
        'count2': count2,
        'count3': count3,
        'count4': count4,
        'count5': count5,
        'types': types,
    }
    return render(req,'tourbuddy/index.html',context)

@login_required(login_url='login_view')
def showdatamore(req):
    trip_type = req.GET.get('type')
    trips = Trip.objects.filter(trip_type=trip_type)
    context = {
        'trips': trips,
        'trip_type': trip_type,
    }
    return render(req, 'tourbuddy/showmore.html', context)


################ Authentication #################
def signup(req):
    if req.method == 'POST':
        form = SignUpforms(req.POST)

        if form.is_valid():
            user = form.save()

            login(req,user)

            return redirect('/')
    else:
        form = SignUpforms()
    return render(req,'tourbuddy/signup.html',{'form':form})

def login_view(req):
    return render(req,'tourbuddy/login.html')

################ details #################
@login_required(login_url='login_view')
def details(req, trip_id):
    data = get_object_or_404(Trip, pk=trip_id)
    
    place = Trip.objects.values('latitude', 'longitude').filter(pk=trip_id).first()

    context = {'place': place, 'data': data}
    return render(req, 'tourbuddy/details.html', context)

################ search_filter #################
@login_required(login_url='login_view')
def search_data(req):
    query = req.GET.get('query')
    results = []
    if query:
        results = Trip.objects.filter(Q(trip_type__icontains=query) | Q(name__icontains=query))
    return render(req,'tourbuddy/index.html',{'query':query,'results':results})


@login_required(login_url='login_view')
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
    return render(request, 'tourbuddy/data_filter.html', context)


################### get_plan #####################

def home_get_plan(request):
    data = Trip.objects.all()
    types = Trip.objects.values('trip_type').distinct()

    trip_filter = TripFilters(request.GET, queryset=Trip.objects.all())

    if 'trip_type' not in request.GET or request.GET['trip_type'] == '':
        trips = Trip.objects.all()
    else:
        
        trips = trip_filter.qs

    paginator = Paginator(trips, 18)
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

    return render(request, 'forplan/home_get_plan.html', {'context':context, 'types': types,'data_page': data_page,'data':data})


def search_data2(req):
    query = req.GET.get('query')
    results = []
    if query:
        results = Trip.objects.filter(Q(trip_type__icontains=query) | Q(name__icontains=query))
    return render(req,'forplan/home_get_plan.html',{'query':query,'results':results})


def data_filter2(request):
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
    return render(request, 'forplan/data_filter_forplan.html', context)

################### TouristNode #####################

def create_TouristNode(req, id):
    tour = Trip.objects.get(pk=id)
    ex_tour = TouristNode.objects.filter(user=req.user, trip=tour).first()

    if not ex_tour:
        TouristNode.objects.create(user=req.user, trip=tour)

    return redirect('/')

def read_TouristNode(request):
    data = TouristNode.objects.filter(user=request.user)
    return render(request,'forplan/cart_plan.html',{'data':data})

def Delete_item(req,id):
    data = TouristNode.objects.get(pk=id)
    data.delete()
    return redirect('read_TouristNode')

################### noti #####################


def Notti(request):
    tourist_node_exists = TouristNode.objects.filter(user=request.user).exists()
    return JsonResponse({'tourist_node_exists': tourist_node_exists})

def Notti0(request):
    n = TouristNode.objects.filter(user=request.user).count()
    return JsonResponse({'n': n})

################### TSP #####################

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


def data_map2(req):
    
    return render(req, 'testtsp/place.html')


# def tsp_christofides(graph):
#     """
#     Find an approximate solution to the Traveling Salesman Problem using the Christofides Algorithm.
#     """
#     cycle = nx.approximation.traveling_salesman.christofides(graph, weight="weight")
#     edge_list = list(nx.utils.pairwise(cycle))
#     tsp_route = edge_list + [edge_list[0]]
#     return tsp_route


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

        return JsonResponse({'tsp_route': tsp_route_coordinates, 'user_location': user_location})
    else:
        return JsonResponse({'error': 'No user location found'})

################### current_location #####################

def current_location(req):
    return render(req,'forplan/current_location.html')


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


def update_current_location(req):
    return render(req,'forplan/update_location.html')

def update_user_location(request):
    if request.method == 'POST':
        # รับค่า user_id และค่า latitude, longitude ที่ต้องการอัพเดตจาก request.POST
        user_id = request.POST.get('user_id')
        latitude = request.POST.get('user_latitude')
        longitude = request.POST.get('user_longitude')
        
        # ค้นหา Order_Trip ทั้งหมดที่ตรงกับ user_id
        order_trips = Order_Trip.objects.filter(user_id=user_id)
        
        # อัพเดตค่า user_latitude และ user_longitude ของ Order_Trip ทุกตัวที่พบ
        for order_trip in order_trips:
            order_trip.user_latitude = latitude
            order_trip.user_longitude = longitude
            order_trip.save()
        
        # สามารถเพิ่มการตอบกลับในรูปแบบ JSON หรือการ redirect ไปยังหน้าที่ต้องการได้ตามความต้องการ
        return redirect('data_map')


@login_required(login_url='login_view')
def data_map(req):
    places = list(TouristNode.objects.filter(user=req.user).select_related('trip').values('trip__latitude', 'trip__longitude','trip__name','trip__image'))

    user_locations = list(Order_Trip.objects.filter(user=req.user).values('user_latitude', 'user_longitude'))

    data = TouristNode.objects.filter(user=req.user)

    context = {'places':places,'user_locations': user_locations,'data':data}
    return render(req, 'forplan/result.html', context)




@login_required(login_url='login_view')
def my_view(request):
    if request.user.is_authenticated:
        custom_url = "https://a4f1-202-176-128-105.ngrok-free.app/data_map/" + str(request.user.id)
        return render(request, 'TourBuddy/result.html', {'custom_url': custom_url})
    else:
        return HttpResponse("กรุณาเข้าสู่ระบบเพื่อเข้าถึงหน้านี้")






# def distrip(req):
#     user_order_trip = Order_Trip.objects.filter(user=req.user).first()
#     if user_order_trip:
#         user_latitude = float(user_order_trip.user_latitude)
#         user_longitude = float(user_order_trip.user_longitude)
#         user_location = (user_latitude,user_longitude)
#         all_distances = {}
        
#         for place in TouristNode.objects.filter(user=req.user):
#             place_location = (float(place.trip.latitude), float(place.trip.longitude))
#             distance = geodesic(user_location, place_location).km
#             all_distances[place] = distance
        
#         return all_distances
#     else:
#         return {}
################### แสดงตัวอย่าง #####################

def distrip2(req):
    user_order_trip = Order_Trip.objects.filter(user=req.user).first()
    if user_order_trip:
        user_latitude = float(user_order_trip.user_latitude)
        user_longitude = float(user_order_trip.user_longitude)
        user_location = (user_latitude, user_longitude)
        all_distances = {}
        
        for place in TouristNode.objects.filter(user=req.user):
            place_location = (float(place.trip.latitude), float(place.trip.longitude))
            distance = geodesic(user_location, place_location).km
            all_distances[place.trip.name] = distance  
        
        return JsonResponse(all_distances)
    else:
        return JsonResponse({})
################### แสดงตัวอย่าง #####################
################### แสดงตัวอย่าง #####################
import math
def get_all_routes_and_places(request):
    user_order_trip = Order_Trip.objects.filter(user=request.user).first()
    if user_order_trip:
        user_location = (float(user_order_trip.user_latitude), float(user_order_trip.user_longitude))

        all_trips = TouristNode.objects.filter(user=request.user)
        cities = {trip.trip.name: trip.trip for trip in all_trips}

        tsp_graph = make_tsp_graph(user_location, cities)

        routes = []
        for edge in tsp_graph.edges(data=True):
            node1 = edge[0]
            node2 = edge[1]

            if node1 == 'User':
                pos1 = user_location
                name1 = 'User Location'
            else:
                pos1 = (cities[node1].latitude, cities[node1].longitude)
                name1 = node1

            if node2 == 'User':
                pos2 = user_location
                name2 = 'User Location'
            else:
                pos2 = (cities[node2].latitude, cities[node2].longitude)
                name2 = node2

            routes.append({'from': pos1, 'from_name': name1, 'to': pos2, 'to_name': name2, 'distance': edge[2]['weight']})

        places = [{'name': trip.trip.name, 'latitude': trip.trip.latitude, 'longitude': trip.trip.longitude} for trip in all_trips]

        num_places = len(cities)
        num_possible_routes = math.factorial(num_places)

        return JsonResponse({'routes': routes, 'places': places, 'user_location': user_location, 'num_possible_routes': num_possible_routes})
    else:
        return JsonResponse({'error': 'No user location found'})


# def make_tsp_graph(user_location, cities):
#     """
#     Create a complete graph representing all possible paths between user location and cities.
#     """
#     G = nx.Graph()

#     G.add_node("User", pos=user_location)

#     for place in cities:
#         G.add_node(place, pos=(cities[place].latitude, cities[place].longitude))
#         print(f"City: {place}, Coordinates: ({cities[place].latitude}, {cities[place].longitude})")

#     for place in cities:
#         distance = geodesic(user_location, (cities[place].latitude, cities[place].longitude)).km
#         G.add_edge("User", place, weight=distance)
#         print(f"Distance from User to {place}: {distance:.2f} km")

#     for place1, place2 in permutations(cities, 2):
#         distance = geodesic((cities[place1].latitude, cities[place1].longitude),
#                             (cities[place2].latitude, cities[place2].longitude)).km
#         G.add_edge(place1, place2, weight=distance)
#         print(f"Distance from {place1} to {place2}: {distance:.2f} km")

#     return G