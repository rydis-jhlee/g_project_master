from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from webapp import views

urlpatterns = [
    # 관리자 상황 조회
    path('admin_search/', views.AdminSearchView.as_view(), name='admin_search'),

    # 라이더 관리자 배송 할당
    path('rider_grant/', views.RiderGrantView.as_view(), name='rider_grant'),
    
    # 인치 시뮬레이터 테스트
    path('simulator/', views.InchSimulatorView.as_view(), name='simulator')

]
