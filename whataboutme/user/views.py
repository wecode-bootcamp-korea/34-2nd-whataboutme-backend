from django.shortcuts import render

# Create your views here.
import json, jwt, re, datetime, pymysql
from django import views

from django.http      import JsonResponse, HttpResponse
from json             import JSONDecodeError
from django.views     import View
from django.db.models import Q
from haversine        import haversine
from decimal          import Decimal

from django.conf      import settings

from motel.models import Motel, Room, Theme, RoomTheme
from reservations.models import Reservation
from motel.utils import distance_cal
from user.models import User

class MakeUser(View):
    def post(self, request):
        
        name = request.GET.get('name')
        kakao_id = request.GET.get('kakao_id')
        nickname = request.GET.get('nickname')
        email = request.GET.get('email')

        User.objects.create(
            name = name,
            kakao_id = kakao_id,
            nickname = nickname,
            email = email
        )

        return JsonResponse({"message" : 'SUCCESS'})