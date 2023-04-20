from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .views import *

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

    # POST(식당 배송 가능 건물 등록)
    # GET(배송 가능 빌딩 조회)
    path("api/sale_connect_agent", SaleConnectAgentAPI.as_view(), name='sale_connect_agent'),

]

