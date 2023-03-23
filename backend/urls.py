
from django.contrib import admin
from django.urls import path
from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 제품 조회, 등록, 수정 ,삭제
    path("backend/product", ProductAPI.as_view(), name='product'),
    # 판매 조회, 등록, 수정 ,삭제
    path("backend/sale_agent", SaleAgentAPI.as_view(), name='sale_agent'),
    # 구매 아이템
    path("backend/buy_item", BuyItemAPI.as_view(), name='buy_item'),

    # 구매 내역, 결제 정보
    #path("backend/sale_agent", SaleAgentAPI.as_view(), name='sale_agent'),
]
