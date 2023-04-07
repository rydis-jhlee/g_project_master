
from django.contrib import admin
from django.urls import path
from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # POST(식당 등록)
    # GET(식당 찾기)
    # GET(마이식당 조회) --> 같이 만들 예정
    # PUT(식당 수정)
    path("api/sale_agent", SaleAgentAPI.as_view(), name='sale_agent'),

    # POST(오늘 식단 등록)
    # GET(오늘 식단 조회)
    # GET(오늘 반찬 메뉴 조회)
    # PUT(오늘 식단 수정)
    path("api/product", ProductAPI.as_view(), name='product'),

    # POST(등록된 오늘 식단 --> 오늘 반찬 메뉴 업데이트)
    path("api/product/update", ProductUpdateAPI.as_view(), name='product_update'),

    # GET(결제 확인)
    # POST(결제 하기)
    path("api/payment", PaymentAPI.as_view(), name='payment'),

    # GET(배송 현황 조회)
    path("api/delivery", DeliveryAPI.as_view(), name='delivery'),

    # 이용자 생성 테스트
    path("api/user", UserAPI.as_view(), name='user'),




]
