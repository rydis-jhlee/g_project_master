
from django.contrib import admin
from django.urls import path
from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [


    # 간편 로그인 테스트 페이지 및 callback
    path('accounts/', include('allauth.urls')),
    path('login/social/kakao', KakaoSignInView.as_view()),
    path('login/social/naver', SocialLoginNaver.as_view()),
    path('logout', LogoutAPI.as_view()),
    path('login', LoginAPI.as_view()),
    path('login/social/callback/kakao', SocialLoginKakaoCallbackAPI.as_view()),
    path('login/social/callback/naver', SocialLoginNaverCallbackAPI.as_view()),
    # path('login/social/callback/apple', SocialLoginAppleCallbackAPI.as_view()),
    # 이용자 생성 테스트
    path("api/user", UserAPI.as_view(), name='user'),

]
