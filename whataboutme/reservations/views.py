import json, datetime, pymysql

from django           import views
from django.http      import JsonResponse, HttpResponse
from json             import JSONDecodeError
from django.views     import View

from motels.models import Room
from reservations.models import Reservation


class MakeReservationView(View):
    def post(self, request):
        try:
            room_id = request.GET.get('room_id')
            user_id = request.GET.get('user_id')
            name = request.GET.get('name')
            checkin = request.GET.get('checkin')
            checkout = request.GET.get('checkout')
            price = Room.objects.filter(id = room_id).values('discount_price')

            Reservation.objects.create(
                room_id = room_id,
                user_id = user_id,
                name = name,
                checkin = checkin,
                checkout = checkout,
                price = price
            )

            return JsonResponse({"message" : 'SUCCESS'}, status = 201)
        
        except JSONDecodeError:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
