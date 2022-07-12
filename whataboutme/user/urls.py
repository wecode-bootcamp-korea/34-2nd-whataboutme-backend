from django.urls import path
# include 제거

from user.views import KakaoGetLoginView, KakaoSignInCallbackView

urlpatterns = [
    path('/kakao/login', KakaoGetLoginView.as_view()),
    path('/kakao/login/callback', KakaoSignInCallbackView.as_view())
]