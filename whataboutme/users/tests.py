import json

from django.test   import TestCase, Client

from unittest      import mock

from users.models    import User
from users.utils     import KaKaoAPI

class KakaoSignInTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.bulk_create(
            [
                User(kakao_id = 2329635456, nickname = "맹주엽"),
                User(kakao_id = 1725915905, nickname = "LITA")
            ]
        )
        
    @mock.patch.object(KaKaoAPI, 'get_user_info')
    @mock.patch.object(KaKaoAPI, 'get_token')
    def test_success_kakao_signin_user(self, mocked_requests1, mocked_requests2):
        client = Client()

        class MockedTokenResponse:
            def json(self):
                return ("rghkasdofkgsjd")
    
        class MockedKakaoUserResponse:
            def json(self):
                return {
                    "id": "1725915905", 
                    "properties": {
                        "nickname": "LITA"
                        }
                }

        mocked_requests1.return_value = MockedTokenResponse().json()
        mocked_requests2.return_value = MockedKakaoUserResponse().json()

        headers = {"HTTP_AUTHORIZATION": "12234524562534", "content_type" : "aplication/json"}
        response = client.get("/v1/api/users/kakao/login/callback", **headers)

        self.assertEqual(response.status_code, 200)

    @mock.patch.object(KaKaoAPI, 'get_user_info')
    @mock.patch.object(KaKaoAPI, 'get_token')
    def test_success_kakao_signup_user(self, mocked_requests1, mocked_requests2):
        client = Client()

        class MockedTokenResponse:
            def json(self):
                return ("rghkasdofkgsjd")
    
        class MockedKakaoUserResponse:
            def json(self):
                return {
                    "id": "246346364", 
                    "properties": {
                        "nickname": "LIZ"
                        }
                }

        mocked_requests1.return_value = MockedTokenResponse().json()
        mocked_requests2.return_value = MockedKakaoUserResponse().json()

        headers = {"HTTP_AUTHORIZATION": "12234524562534", "content_type" : "aplication/json"}
        response = client.get("/v1/api/users/kakao/login/callback", **headers)

        self.assertEqual(response.status_code, 201)
