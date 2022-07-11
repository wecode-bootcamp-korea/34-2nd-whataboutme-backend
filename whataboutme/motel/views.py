import json, jwt, re, datetime, pymysql

from django.http      import JsonResponse, HttpResponse
from json             import JSONDecodeError
from django.views     import View
from django.db.models import Q
from haversine import haversine

from django.conf      import settings

from motel.models import Motel, Room, Reservation, Theme, RoomTheme


class MotelListQuery(View) : 
    def get(self, request):
        try : 
            my_location = request.GET.get('my_location')
            distance = request.GET.get('distance')
            themes = request.GET.getlist('themes[]')
            checkinout = request.GET.get('checkinout')
            price = request.GET.get('price')

            q = Q()

            if my_location : 
                my_latitude, my_longitude = list(map(str, my_location))
            if distance :
                q &= Q(distance = distance)
            if themes :
                q &= Q(themes = themes[])
            if checkinout : 
                checkin, checkout = list(map(str, checkinout))
            if price:
                pricemin, pricemax = list(map(str, price))

            print (q)

            motel_query = Room.objects.filter(q) \
                .prefetch_related('motel', 'reservation_room', 'room_theme' )

            # motel = 룸과 연결된 모텔
            # reservation_room = 예약 
            # room_theme = 룸테마



            results = [
                {
                    'id' : room.motel.id,
                    'name' : room.motel.name,
                    'address' : room.motel.address,
                    'price' : room.discount_price.first()

                } for room in motel_query
            ]
        except JSONDecodeError:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

