
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
    # 구매 등록
    path("backend/buy", BuyAPI.as_view(), name='buy'),
    # 결제 전처리 --> 배송테이블 등록 --> 총 구매제품 합산된 결제금액등 정보 추가
    path("backend/payment/preProcess", PaymentPreProcessAPI.as_view(), name='pre_process'),
    # 결제 후처리 --> 결제, 배송, 제품(수량) 업데이트
    path("backend/payment/postProcess", PaymentPostProcessAPI.as_view(), name='post_process'),








    # 구매 내역, 결제 정보
    #path("backend/sale_agent", SaleAgentAPI.as_view(), name='sale_agent'),
]
