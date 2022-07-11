import json, jwt, re, datetime, pymysql

from django.http      import JsonResponse, HttpResponse
from django.views     import View
from django.db.models import Q
from haversine import haversine

from django.conf      import settings

from motel.models import Motel, Room, Reservation, Theme, RoomTheme

from 

my_location = (37.506293718576, 127.05370511256017)
motel_location = (37.502427594190884, 127.03846302471605)

distance = haversine(my_location, motel_location, unit = 'km')

class MotelListQuery(View) : 
    def get(self, request):
        distance = request.GET.get('distance')
        theme_id = request.GET.getlist('theme[]')
        checkout = request.GET.get('checkout')
        checkint = request.GET.get('checkin')
        # price = request.GET.get('price')

        q = Q()

        # if theme_id :
        #     q &= Q(theme_id = theme_id)
        # 리스트가 일치해야함 

        motel_query = Room.objects.filter(q) \
            .prefetch_related('motel', 'motel__room', 'room__room_theme')

        # motel = 룸과 연결된 모텔
        # motel__room = Reservation
        # room__room_theme = 룸테마

        results = [
            {
                'id' : room.motel.id,
                'name' : 
            } for room in motel_query
        ]


