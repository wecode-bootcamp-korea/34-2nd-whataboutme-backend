from django.http import JsonResponse
import json, datetime, jwt

from django.shortcuts import render
import requests

from django.shortcuts import redirect
from django.views import View

from django.conf  import settings

from json import JSONDecodeError

from user.models import User

sample_ip = 'http://127.0.0.1:8000'

class KakaoGetLoginView(View):
    def get(self, request):
        CLIENT_ID = settings.KAKAO_OAUTH_KEY['KAKAO_REST_API_KEY']
        REDIRECT_URL = settings.KAKAO_OAUTH_KEY['KAKAO_REDIRECT_URL']
        url = "https://kauth.kakao.com/oauth/authorize?client_id={0}&redirect_uri={1}&response_type=code".format(CLIENT_ID, REDIRECT_URL)
        result = redirect(url)

        return result

class KakaoSignInCallbackView(View):
    def get(self, request):
        auth_code = request.GET.get('code')
        kakao_token_api = 'https://kauth.kakao.com/oauth/token'
        data = {
            'grant_type' : 'authorization_code',
            'client_id' : settings.KAKAO_OAUTH_KEY['KAKAO_REST_API_KEY'],
            'redirect_url' : settings.KAKAO_OAUTH_KEY['KAKAO_REDIRECT_URL'],
            'code' : auth_code
        }
        
        token_response = requests.post(kakao_token_api, data=data)
        access_token = token_response.json().get('access_token')
        kakao_user_response = requests.get('https://kapi.kakao.com/v2/user/me', headers={"Authorization" : f'Bearer ${access_token}'})
        data = kakao_user_response.json()

        try:

            if not User.objects.filter(kakao_id = data['id']).exists():
                User.objects.create(
                kakao_id = data['id'],
                nickname = data['properties']['nickname']
                )
                pass


            user = User.objects.get(kakao_id = data['id'])
        
            authorization_token = jwt.encode({'user_id' : user.id}, settings.SECRET_KEY, algorithm='HS256')
        
            return JsonResponse({"message" : "LOGIN_SUCCESS", "authorization_token" : authorization_token}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        except JSONDecodeError:
            return JsonResponse({"message": "JSON_DECODE_ERROR"}, status=400)



        


# class SignInView(KakaoSignInCallbackView):
#     def post(self, data):
#         try:
#             kakao_id = data['id']
#             nickname = data['properties']['nickname']

#             if User.objects.filter(kakao_id = data['id']).exists():
#                 user = User.objects.get(kakao_id = data['id'])
#                 authorization_token = jwt.encode({'user_id' : user.id}, settings.SECRET_KEY, algorithm='HS256')

#                 return JsonResponse({"message" : "LOGIN_SUCCESS", "authorization_token" : authorization_token}, status=200)
            
#             else :
#                 return JsonResponse({"message" : "LOGIN_FAILED"}, status=400)

#         except KeyError:
#             return JsonResponse({"message": "KEY_ERROR"}, status=400)
#         except JSONDecodeError:
#             return JsonResponse({"message": "JSON_DECODE_ERROR"}, status=400)

# class SignUpView(View):
#     def post(self, data):
#         try:
#             kakao_id = data['id']
#             nickname = nickname = data['properties']['nickname']

#             User.objects.create(
#                 kakao_id = kakao_id,
#                 nickname = nickname
#             )

#             res = requests.post('{0}/user/signin'.format(sample_ip), data=data)
#             return res
        
#         except KeyError:
#             return JsonResponse({"message": "KEY_ERROR"}, status=400)
#         except JSONDecodeError:
#             return JsonResponse({"message": "JSON_DECODE_ERROR"}, status=400)