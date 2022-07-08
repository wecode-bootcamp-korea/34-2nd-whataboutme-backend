from django.urls import path, include

from user.views import KakaoGetLoginView, KakaoSignInCallbackView
urlpatterns = [
    path('/kakao/login', KakaoGetLoginView.as_view()),
    path('/kakao/login/callback', KakaoSignInCallbackView.as_view())
]