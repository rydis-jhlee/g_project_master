from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    # GET(배송 현황 조회) TODO: API 변경으로 수정 생성해야됨
    # path("api/delivery", DeliveryAPI.as_view(), name='delivery'),

    # POST(배달기사 픽업 수령)
    # GET(배달기사 픽업 조회)
    path("api/delivery/management", DeliveryManagementAPI.as_view(), name='delivery_pickup'),

    # POST(배달기사 배송완료)
    path("api/delivery_complete", DeliveryCompleteAPI.as_view(), name='delivery_complete'),

    # POST(배달기사 콜업)
    path("api/delivery_callup", DeliveryCallUpAPI.as_view(), name='delivery_callup'),
    
    # 관리자페이지 배송현황 호출
    path("api/delivery_dashboard", DeliveryDashboardAPI.as_view(), name='delivery_dashboard'),

    # 배달기사 현황조회
    path("api/delivery/user", DeliveryUserAPI.as_view()),

]

