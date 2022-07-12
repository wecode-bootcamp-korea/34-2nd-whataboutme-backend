import json, datetime, jwt, requests

from django.http      import JsonResponse
from django.shortcuts import redirect
from django.views     import View
from django.conf      import settings

from user.models import User
from core.utils  import KaKaoAPI
# 모듈 import convention 정리

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
            
            # get_or_create 메소드 써서 리팩토링 꼭 해보기
            if not User.objects.filter(kakao_id = kakao_user_info['id']).exists():
                User.objects.create(
                kakao_id = kakao_user_info['id'],
                nickname = kakao_user_info['properties']['nickname']
                )
                pass

            '''
            user, is_created = User.objects.get_or_create(
                ... = ...
                ... = ...
                defaults = {
                    '...' : ... ,
                    '...' : ... 
                }
            )
            '''

            user = User.objects.get(kakao_id = kakao_user_info['id'])
        
            access_token = jwt.encode({'user_id' : user.id}, settings.SECRET_KEY, algorithm='HS256')
            
            return JsonResponse({"message" : "LOGIN_SUCCESS", "access_token" : access_token}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)



        


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