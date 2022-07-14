import requests

from django.shortcuts import redirect

from core.models import TimestampZone, tomorrow

class KaKaoAPI:
    def __init__(self, rest_api_key, redirect_url):
        self.rest_api_key = rest_api_key
        self.redirect_url = redirect_url

    def get_auth_code(self):
        url = "https://kauth.kakao.com/oauth/authorize?client_id={0}&redirect_uri={1}&response_type=code".format(self.rest_api_key, self.redirect_url)

        return url

    def get_token(self, auth_code):
        url  = 'https://kauth.kakao.com/oauth/token'
        data = {
            'grant_type'   : 'authorization_code',
            'client_id'    : self.rest_api_key,
            'redirect_url' : self.redirect_url,
            'code'         : auth_code
        }

        response = requests.post(url, data=data)

        return response.json().get('access_token')

    def get_user_info(self, token):
        url     = 'https://kapi.kakao.com/v2/user/me'
        headers = {"Authorization" : f'Bearer ${token}'}

        response = requests.get(url, headers=headers)

        return response.json()