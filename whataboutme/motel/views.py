from django.shortcuts import render

import pymysql
from haversine import haversine

# Create your views here.

my_location = (37.506293718576, 127.05370511256017)
motel_location = (37.502427594190884, 127.03846302471605)

distance = haversine(my_location, motel_location, unit = 'km')