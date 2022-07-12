import json

from django.test   import TestCase, Client
# from unittest.mock import patch, MagicMock
from unittest      import mock

from .models    import User
from core.utils import KaKaoAPI

class KakaoSignInTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.bulk_create(
            [
                User(kakao_id = 2329635456, nickname = "맹주엽"),
            ]
        )
        
    # 로그인 성공 환경 파악
    # @patch("user.views.requests")
    @mock.patch.object(KaKaoAPI, 'get_user_info')
    @mock.patch.object(KaKaoAPI, 'get_token')
    def test_success_kakao_signin_signup_user(self, mocked_requests1, mocked_requests2):
        client = Client()

        class MockedTokenResponse:
            def json(self):
                return ("ZlAggIGWGDjLsA0HxlJXMaeDzaIDjhCfVMdxPOytCilvuAAAAYHctaVw")
    
        class MockedKakaoUserResponse:
            def json(self):
                return {
                    "id": "2329635456", 
                    "properties": {
                        "nickname": "맹주엽"
                        }
                }

        mocked_requests1.return_value = MockedTokenResponse().json()
        mocked_requests2.return_value = MockedKakaoUserResponse().json()

        response = client.get("/user/kakao/login/callback", **{"HTTP_AUTHORIZATION": "12234524562534", "content_type" : "aplication/json"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(), 
            {
                "message" : "LOGIN_SUCCESS", "access_token" : "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxfQ.-cIvMFu7SwFarij-akTUExGhcvfG_UDxNktKJOFEhfg"
            }
        )