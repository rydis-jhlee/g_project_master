
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

    # 결제 처리 --> 배송테이블 등록 --> 구매건수에 대해 합쳐서 결제금액등 정보 넣어야함.








    # 구매 내역, 결제 정보
    #path("backend/sale_agent", SaleAgentAPI.as_view(), name='sale_agent'),
]
