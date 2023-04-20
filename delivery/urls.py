from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    # GET(배송 현황 조회)
    path("api/delivery", DeliveryAPI.as_view(), name='delivery'),

    # POST(배달기사 픽업 수령)
    # GET(배달기사 픽업 조회)
    path("api/delivery_pickup", DeliveryPickUpAPI.as_view(), name='delivery_pickup'),

    # POST(배달기사 배송완료)
    path("api/delivery_complete", DeliveryCompleteAPI.as_view(), name='delivery_complete'),

    # POST(배달기사 콜업)
    path("api/delivery_callup", DeliveryCallUpAPI.as_view(), name='delivery_callup'),

]

