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
            themes = []
            my_latitude = request.GET.get('my_latitude')
            my_longitude = request.GET.get('my_longitude')
            distance = request.GET.get('distance')
            themes_list = request.GET.getlist("themes[]", None)
            checkin = request.GET.get('checkin')
            checkout = request.GET.get('checkout')
            pricemin = request.GET.get('pricemin')
            pricemax = request.GET.get('pricemax')

            q = Q()
            
            print(themes_list)

        #     motel_query = Room.objects.filter(q) \
        #         .prefetch_related('motel', 'reservation_room', 'room_theme' )

        #     # motel = 룸과 연결된 모텔
        #     # reservation_room = 예약 
        #     # room_theme = 룸테마



        #     results = [
        #         {
        #             'id' : room.motel.id,
        #             'name' : room.motel.name,
        #             'address' : room.motel.address,
        #             'price' : room.discount_price.first()

        #         } for room in motel_query
        #     ]
            return JsonResponse({"message": 'SUCCESS', "theme": themes_list, "checkin":checkin, "checkout":checkout}, status=200)
        except JSONDecodeError:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

