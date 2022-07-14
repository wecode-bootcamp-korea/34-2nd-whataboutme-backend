import json, datetime, jwt, requests

from django.http      import JsonResponse
from django.shortcuts import redirect
from django.views     import View
from django.conf      import settings

from users.models import User
from users.utils  import KaKaoAPI

class KakaoGetLoginView(View):
    def get(self, request):
        url = KaKaoAPI(settings.KAKAO_OAUTH_KEY['KAKAO_REST_API_KEY'], settings.KAKAO_OAUTH_KEY['KAKAO_REDIRECT_URL']).get_auth_code()

        return redirect(url)

class KakaoSignInCallbackView(View):
    def get(self, request):
        try:
            auth_code = request.GET.get('code')
            
            kakao           = KaKaoAPI(settings.KAKAO_OAUTH_KEY['KAKAO_REST_API_KEY'], settings.KAKAO_OAUTH_KEY['KAKAO_REDIRECT_URL'])
            kakao_token     = kakao.get_token(auth_code)
            kakao_user_info = kakao.get_user_info(kakao_token)
                        
            user, is_created = User.objects.get_or_create(
                kakao_id     = kakao_user_info['id'],
                nickname     = kakao_user_info['properties']['nickname']
            )

            user = User.objects.get(kakao_id = kakao_user_info['id'])
            access_token = jwt.encode({'user_id' : user.id}, settings.SECRET_KEY, algorithm='HS256')

            if is_created == False:
                return JsonResponse({"message" : "LOGIN_SUCCESS", "access_token" : access_token}, status=200)
            if is_created == True:
                return JsonResponse({"message" : "WELCOME", "access_token" : access_token}, status=201)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

class MakeUser(View):
    def post(self, request):
        try :
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

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
