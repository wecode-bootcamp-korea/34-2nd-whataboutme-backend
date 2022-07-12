import json, jwt, re, datetime, pymysql

from django.http      import JsonResponse, HttpResponse
from json             import JSONDecodeError
from django.views     import View
from django.db.models import Q
from haversine import haversine
from decimal import Decimal

from django.conf      import settings

from motel.models import Motel, Room, Reservation, Theme, RoomTheme


class MotelListQuery(View) : 
    def get(self, request):
        try : 
            my_latitude = float(request.GET.get('my_latitude'))
            my_longitude = float(request.GET.get('my_longitude'))
            distance = request.GET.get('distance')
            theme_list = request.GET.getlist("theme", None)
            checkin = request.GET.get('checkin')
            checkout = request.GET.get('checkout')
            pricemin = request.GET.get('pricemin')
            pricemax = request.GET.get('pricemax')

            q = Q()

            # 거리 필터링
            if my_latitude and my_longitude :
                q &= Q(motel__latitude__range = (my_latitude - 0.025, my_latitude + 0.025 )) 
                q &= Q(motel__longitude__range = (my_longitude - 0.035, my_longitude + 0.035))
                #range 함수 문제

            # 테마 필터링

            # 체크인아웃 필터링
            if checkin and checkout :
                q &= ~((Q(reservation_room__checkout__gt = checkin) & Q(reservation_room__checkin__lte = checkin)) |
                Q(reservation_room__checkin__range = [checkin, checkout]))

            #가격 필터링
            if pricemin and pricemax :
                q &= (Q(discount_price__gte = pricemin) & Q(discount_price__lte = pricemax))

            motel_query = Room.objects.filter(q) \
                .prefetch_related('motel', 'reservation_room', 'room_theme' )


        #     # motel = 룸과 연결된 모텔
        #     # reservation_room = 예약 
        #     # room_theme = 룸테마
            


            results = [
                {
                    'id' : room.motel.id,
                    'name' : room.motel.name,
                    'address' : room.motel.address,

                } for room in motel_query
            ]
            return JsonResponse({"message": 'SUCCESS', 'result' : results}, status=200)
        except JSONDecodeError:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

