from django.shortcuts import render,redirect,get_object_or_404
from tourbuddy.models import *
from .forms import *
import django_filters
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test



# Create your views here.
class TripFilters(django_filters.FilterSet):
    trip_type = django_filters.CharFilter(field_name='trip_type', lookup_expr='iexact')

    class Meta:
        model = Trip
        fields = ['trip_type']

def admin_page(request):
    if not request.user.is_superuser:
        return redirect('indexcard1')

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

    return render(request, 'admin_page.html', {'context':context, 'types': types,'data_page': data_page,'data':data})

@login_required
def list_users(request):
    users = User.objects.all()
    context = {
        'users': users,
    }
    return render(request, 'list_users.html', context)


@login_required
def create_trip(request):
    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_page')
    else:
        form = TripForm()

    return render(request, 'create.html', {'form': form})


@login_required
def update_trip(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    if request.method == 'POST':
        form = TripForm(request.POST, instance=trip)
        if form.is_valid():
            form.save()
            return redirect('admin_page')
    else:
        form = TripForm(instance=trip)

    return render(request, 'update.html', {'form': form})

def delete_trip(req,id):
    data = Trip.objects.get(pk=id)
    data.delete()
    return redirect('admin_page')


@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('list_users')

    return render(request, 'delete_user.html', {'user': user})