from django.db import models
from django.utils import timezone

from decimal import Decimal

from datetime import timedelta
from haversine import haversine

def distance_cal (my_latitude, my_longitude, motel_latitude, motel_longitude):
    my_location = (my_latitude, my_longitude)
    motel_location = (motel_latitude, motel_longitude)
    
    distance = haversine(my_location, motel_location, unit = 'km')

    return distance