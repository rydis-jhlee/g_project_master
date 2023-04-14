
from django.contrib import admin
from django.urls import path
from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # POST(식당 등록)
    # GET(식당 찾기)
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

    # POST(마이식당 등록, 수정)
    # GET(마이식당 등록된 이용자 조회) --> 판매 관리자가 볼 수 있는 화면
    path("api/my_restaurant", MyRestaurantAPI.as_view(), name='my_restaurant'),
    
    # POST(식당 배송 가능 건물 등록)
    # GET(배송 가능 빌딩 조회)
    path("api/sale_connect_agent", SaleConnectAgentAPI.as_view(), name='sale_connect_agent'),

    # POST(배달기사 픽업 수령)
    # GET(배달기사 픽업 조회)
    path("api/delivery_pickup", DeliveryPickUpAPI.as_view(), name='delivery_pickup'),
    
    # POST(배달기사 배송완료)
    path("api/delivery_complete", DeliveryCompleteAPI.as_view(), name='delivery_complete'),

    # POST(결제 취소)
    path("api/payment_cancel", PaymentCancelAPI.as_view(), name='payment_cancel'),
    
    # GET(주문 내용 확인)
    path("api/payment_list", PaymentListAPI.as_view(), name='payment_list'),

    # 판매 현황 테스트
    path("api/order_stat", OrderStatAPI.as_view(), name='order_stat'),


    # OrderModifyAPI 주문수정하는 api인데 수량변경 같은건 front에서 하면될것 같아서 사용 중지


]
