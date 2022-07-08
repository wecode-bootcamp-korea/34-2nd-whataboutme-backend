import json, unittest
from urllib import response

from django.test import TestCase, Client
from unittest.mock import patch, MagicMock

from .models import User

class KakaoSignInTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.bulk_create(
            [User(kakao_id = 2329635456, nickname = "맹주엽"),
            
            ]
        )
    # 로그인 성공 환경 파악
    @patch("user.views.requests")
    def test_success_kakao_signin_signup_user(self, mocked_requests1, mocked_requests2):
        c = Client()

        class TokenResuests:
            def json(self):
                return ("ZlAggIGWGDjLsA0HxlJXMaeDzaIDjhCfVMdxPOytCilvuAAAAYHctaVw")
        mocked_requests1.post = MagicMock(return_value1 = TokenResuests())

        class KakaoUserResponse:
            def json(self):
                return {
                    "id": "2329635456", 
                    "properties": {
                        "nickname": "맹주엽"
                        }
                }
        mocked_requests2.get = MagicMock(return_value2 = KakaoUserResponse())

        test = {"id": "2329635456", 
                    "properties": {"nickname": "맹주엽"}}

       # headers =  {"HTTP_AUTHORIZATION": "12234524562534", "content_type" : "aplication/json"}
        response = c.get("/user/kakao/callback", json.dumps(test), **{"HTTP_AUTHORIZATION": "12234524562534", "content_type" : "aplication/json"})


        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(), 
            {
                "message" : "LOGIN_SUCCESS", "authorization_token" : "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxfQ.-cIvMFu7SwFarij-akTUExGhcvfG_UDxNktKJOFEhfg"
            }
        )