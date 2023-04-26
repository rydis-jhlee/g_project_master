from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [

    # GET(식당 찾기)
    path("api/store", SaleAgentAPI.as_view()),
    # POST(식당 등록)
    path("api/store/create", SaleAgentCreateAPI.as_view()),
    # POST(식당 수정)
    path("api/store/update", SaleAgentUpdateAPI.as_view()),


    # GET(오늘 식단 조회)
    # GET(오늘 반찬 메뉴 조회)
    path("api/product", ProductAPI.as_view()),
    # POST(오늘 식단 등록)
    path("api/product/create", ProductCreateAPI.as_view()),

    # PUT(오늘 식단 수정)
    # POST(등록된 오늘 식단 --> 오늘 반찬 메뉴 업데이트)
    path("api/product/update", ProductUpdateAPI.as_view()),

    # GET(배송 가능 빌딩 조회)
    path("api/sale_addr", SaleConnectAgentAPI.as_view()),

    # POST(식당 배송 가능 건물 등록)
    path("api/sale_addr/create", StoreAddrCreate.as_view()),

]

