from django.urls import path

from users.views import KakaoGetLoginView, KakaoSignInCallbackView

urlpatterns = [
    path('/kakao/login', KakaoGetLoginView.as_view()),
    path('/kakao/login/callback', KakaoSignInCallbackView.as_view()),
]