import json, jwt, re, datetime, pymysql

from django.http      import JsonResponse, HttpResponse
from json             import JSONDecodeError
from django.views     import View
from django.db.models import Q
from haversine        import haversine
from decimal          import Decimal

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
            # distance에 따라 사전 쿼리값변견
            if my_latitude and my_longitude :
                q &= Q(latitude__range = (my_latitude - 0.025, my_latitude + 0.025 )) 
                q &= Q(longitude__range = (my_longitude - 0.035, my_longitude + 0.035))
            

            # 테마 필터링(
            if theme_list : 
                q &= Q(rooms__roomthemes_theme__in = theme_list )

            # 체크인아웃 필터링
            if checkin and checkout :
                q &= ~((Q(rooms__reservationrooms_checkout__gt = checkin) & Q(rooms__reservationrooms_checkin__lte = checkin)) |
                Q(rooms__reservationrooms__checkin__range = [checkin, checkout]))

            #가격 필터링
            if pricemin and pricemax :
                q &= Q(rooms__discount_price__gte = pricemin)
                q &= Q(rooms__discount_price__lte = pricemax)

            # 쿼리(모텔기준으로 해야함)
            motels = Motel.objects.filter(q) \
                .prefetch_related('rooms', 'rooms__reservationrooms', 'rooms__roomthemes').order_by('id').distinct() \
                .annotate()


            # motel = 룸과 연결된 모텔
            # reservation_room = 예약 
            # room_theme = 룸테마


            results = [
                {
                    'id' : motel.id,
                    'name' : motel.name,
                    'address' : motel.address,

                } for motel in motels
            ]
            return JsonResponse({"message": 'SUCCESS', 'result' : results}, status=200)
        except JSONDecodeError:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

