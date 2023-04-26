from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    # GET(결제 확인)
    # POST(결제 하기)
    path("api/payment", PaymentAPI.as_view(), name='payment'),

    # POST(결제 완료)
    path("api/payment_completion", PaymentCompletion.as_view()),

    # POST(결제 취소)
    path("api/payment_cancel", PaymentCancelAPI.as_view(), name='payment_cancel'),

    # GET(주문 상세 페이지)
    path("api/payment/detail", PaymentDetailAPI.as_view()),

    # GET(주문 내용 확인)
    path("api/payment/list", PaymentListAPI.as_view(), name='payment_list'),

    # 관리자페이지 결제현황 호출
    path("api/admin_dashboard", AdminDashboardAPI.as_view(), name='admin_dashboard'),



]
