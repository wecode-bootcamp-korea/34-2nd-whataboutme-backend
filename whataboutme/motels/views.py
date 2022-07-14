import json, jwt, re, datetime, pymysql

from django           import views
from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q
from django.conf      import settings
from django.db.models import Max, Min, Avg

from haversine        import haversine
from decimal          import Decimal

from motels.models       import Motel, Room, Theme, RoomTheme
from reservations.models import Reservation
from core.utils          import distance_cal


class MotelListQuery(View) : 
    def get(self, request):
        try : 
            my_latitude  = float(request.GET.get('my_latitude'))
            my_longitude = float(request.GET.get('my_longitude'))
            # distance     = request.GET.get('distance')
            theme        = request.GET.get("theme")
            checkin      = request.GET.get('checkin')
            checkout     = request.GET.get('checkout')
            pricemin     = request.GET.get('pricemin')
            pricemax     = request.GET.get('pricemax')

            q = Q()
            q1 = Q()

            if my_latitude and my_longitude :
                q &= Q(latitude__range = (my_latitude - 0.025, my_latitude + 0.025 )) 
                q &= Q(longitude__range = (my_longitude - 0.035, my_longitude + 0.035))
            
            if theme : 
                q &= Q(roomthemes__theme = theme)

            if checkin and checkout :
                q1 &= (
                    Q(checkin__gte= checkin) &
                    Q(checkout__lte = checkout)
                )

            if pricemin and pricemax :
                q &= Q(rooms__discount_price__gte = pricemin)
                q &= Q(rooms__discount_price__lte = pricemax)


            reservations = Reservation.objects.filter(q1)

            motel_list = Motel.objects.filter(q).exclude(rooms__reservationrooms__in=reservations).order_by('id').distinct() \
                .prefetch_related('rooms', 'rooms__roomthemes', 'rooms__reservationrooms' )
                        

            results = [
                {
                    'motelid' : motel.id,
                    'name' : motel.name,
                    'address' : motel.address,
                    'distance' : distance_cal(my_latitude, my_longitude, motel.latitude, motel.longitude)
                } for motel in motel_list
            ]
            return JsonResponse({"message": 'SUCCESS', 'result' : results}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

class RoomListView(View):
    def get(self, request):
        try :
            motel_id = request.GET.get('motel_id')
            checkin = request.GET.get('checkin')
            checkout = request.GET.get('checkout')

            q = Q()
            q1  = Q()

            if motel_id :
                q &= Q(motel_id = motel_id)

            if checkin and checkout :
                q1 &= (
                    Q(checkin__gte=checkin) &
                    Q(checkout__lte = checkout)
                )

            reservations = Reservation.objects.filter(q1)

            room_list = Room.objects.filter(q).exclude(reservationrooms__in=reservations) \
                .prefetch_related('motel', 'roomthemes', 'reservationrooms' )
                #.order_by('id').distinct() \
                #.annotate()

            print(room_list)

            results = [
                {
                    'id' : room.id,
                    'name' : room.name,
                    'motel' : room.motel.name,
                } for room in room_list
            ]
            return JsonResponse({"message": 'SUCCESS', 'result' : results}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)