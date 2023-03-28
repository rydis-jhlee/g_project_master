
from django.contrib import admin
from django.urls import path
from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 제품 조회, 등록, 수정 ,삭제
    path("backend/product", ProductAPI.as_view(), name='product'),
    # 판매 업체 조회, 등록, 수정 ,삭제
    path("backend/sale_agent", SaleAgentAPI.as_view(), name='sale_agent'),
    # 구매 등록 --> 결제테이블 생성, 구매 아이템 갯수만큼 추가
    path("backend/buy", BuyAPI.as_view(), name='buy'),
    # 구매 수정 --> 구매할 수량, 총제품수량 변경
    path("backend/buy/modify", BuyModifyAPI.as_view(), name='buy_modify'),
    # 구매 취소

    # 결제 처리 --> 결제 정보, 제품(수량) 업데이트, 배송테이블 생성 
    path("backend/payment", PaymentAPI.as_view(), name='payment'),

    # 결제 전처리 --> 배송테이블 등록 --> 총 구매제품 합산된 결제금액 정보 추가 --> 결제 처리로 통합
    #path("backend/payment/preProcess", PaymentPreProcessAPI.as_view(), name='pre_process'),

]
